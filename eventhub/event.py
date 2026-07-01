from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from datetime import datetime
from .models import Event, Comment, EventStatus
from .forms import EventForm, CommentForm
from . import db

event_bp = Blueprint("event", __name__)


# ============================================================
#  Helper: auto-update event status based on date/tickets
# ============================================================
def refresh_event_status(event):
    """Automatically update event status:
    - Do NOT override Cancelled (creator sets that manually).
    - If available_tickets == 0 -> Sold Out
    - If event date has passed  -> Inactive
    - Otherwise                  -> Open
    """
    if event.status == EventStatus.CANCELLED:
        return
    if event.available_tickets <= 0:
        event.status = EventStatus.SOLD_OUT
    elif event.date < datetime.now():
        event.status = EventStatus.INACTIVE
    else:
        # Only restore to Open if it was auto-set (not Cancelled)
        if event.status in (EventStatus.INACTIVE, EventStatus.SOLD_OUT):
            # Re-check: tickets available again or date in future?
            if event.available_tickets > 0 and event.date >= datetime.now():
                event.status = EventStatus.OPEN


# ============================================================
#  Event list (with category filter)
# ============================================================
@event_bp.route("/events")
def list_events():
    """Browse all events with optional category filter and search."""
    category = request.args.get("category", "", type=str)
    search = request.args.get("search", "", type=str).strip()

    query = db.select(Event).order_by(Event.date.asc())
    if category:
        query = query.where(Event.category == category)
    if search:
        query = query.where(Event.name.ilike(f"%{search}%"))
    events = db.session.scalars(query).all()

    # Refresh statuses for display
    changed = False
    for ev in events:
        old = ev.status
        refresh_event_status(ev)
        if ev.status != old:
            changed = True
    if changed:
        db.session.commit()

    return render_template(
        "event/list.html",
        events=events,
        selected_category=category,
        search_query=search,
    )


# ============================================================
#  Event detail (with comments)
# ============================================================
@event_bp.route("/events/<int:event_id>")
def event_detail(event_id):
    """View a single event's details and comments."""
    event = db.session.get(Event, event_id)
    if event is None:
        flash("Event not found.", "danger")
        return redirect(url_for("event.list_events"))

    # Refresh status
    refresh_event_status(event)
    db.session.commit()

    # Fetch comments ordered by newest first
    comments = db.session.scalars(
        db.select(Comment)
        .where(Comment.event_id == event_id)
        .order_by(Comment.created_at.desc())
    ).all()

    comment_form = CommentForm()
    is_creator = current_user.is_authenticated and current_user.id == event.user_id
    can_book = (
        current_user.is_authenticated
        and event.status == EventStatus.OPEN
        and event.available_tickets > 0
    )

    return render_template(
        "event/detail.html",
        event=event,
        comments=comments,
        comment_form=comment_form,
        is_creator=is_creator,
        can_book=can_book,
        EventStatus=EventStatus,
    )


# ============================================================
#  Create event
# ============================================================
@event_bp.route("/events/create", methods=["GET", "POST"])
@login_required
def create_event():
    """Create a new event (logged-in users only)."""
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            name=form.name.data,
            description=form.description.data,
            category=form.category.data,
            date=form.date.data,
            venue=form.venue.data,
            price=form.price.data,
            total_tickets=form.total_tickets.data,
            available_tickets=form.total_tickets.data,  # initially all available
            status=EventStatus.OPEN,
            image=form.image.data if form.image.data else None,
            user_id=current_user.id,
        )
        db.session.add(event)
        db.session.commit()

        flash(f'Event "{event.name}" created successfully!', "success")
        return redirect(url_for("event.event_detail", event_id=event.id))

    return render_template("event/create.html", form=form)


# ============================================================
#  Update event (creator only)
# ============================================================
@event_bp.route("/events/<int:event_id>/update", methods=["GET", "POST"])
@login_required
def update_event(event_id):
    """Update event details (creator only). Cannot change status."""
    event = db.session.get(Event, event_id)
    if event is None:
        flash("Event not found.", "danger")
        return redirect(url_for("event.list_events"))

    if event.user_id != current_user.id:
        flash("You can only edit events you created.", "danger")
        return redirect(url_for("event.event_detail", event_id=event_id))

    form = EventForm(obj=event) if request.method == "GET" else EventForm()

    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        event.category = form.category.data
        event.date = form.date.data
        event.venue = form.venue.data
        event.price = form.price.data
        event.image = form.image.data if form.image.data else None

        # If total_tickets increased, add the difference to available_tickets
        new_total = form.total_tickets.data
        if new_total != event.total_tickets:
            diff = new_total - event.total_tickets
            event.available_tickets = max(0, event.available_tickets + diff)
            event.total_tickets = new_total

        # Refresh auto-status (do not override Cancelled)
        refresh_event_status(event)

        db.session.commit()
        flash("Event updated successfully.", "success")
        return redirect(url_for("event.event_detail", event_id=event.id))

    return render_template("event/update.html", form=form, event=event)


# ============================================================
#  Cancel event (creator only)
# ============================================================
@event_bp.route("/events/<int:event_id>/cancel", methods=["POST"])
@login_required
def cancel_event(event_id):
    """Cancel an event (creator only)."""
    event = db.session.get(Event, event_id)
    if event is None:
        flash("Event not found.", "danger")
        return redirect(url_for("event.list_events"))

    if event.user_id != current_user.id:
        flash("You can only cancel events you created.", "danger")
        return redirect(url_for("event.event_detail", event_id=event_id))

    if event.status == EventStatus.CANCELLED:
        flash("This event is already cancelled.", "info")
        return redirect(url_for("event.event_detail", event_id=event_id))

    event.status = EventStatus.CANCELLED
    db.session.commit()
    flash(f'Event "{event.name}" has been cancelled.', "warning")
    return redirect(url_for("event.event_detail", event_id=event_id))


# ============================================================
#  Add comment (logged-in users only)
# ============================================================
@event_bp.route("/events/<int:event_id>/comment", methods=["POST"])
@login_required
def add_comment(event_id):
    """Add a comment to an event (logged-in users only)."""
    event = db.session.get(Event, event_id)
    if event is None:
        flash("Event not found.", "danger")
        return redirect(url_for("event.list_events"))

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            event_id=event_id,
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment posted.", "success")
    else:
        flash("Comment cannot be empty.", "danger")

    return redirect(url_for("event.event_detail", event_id=event_id))
