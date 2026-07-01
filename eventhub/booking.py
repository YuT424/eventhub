from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from .models import Booking, Event, EventStatus
from .forms import BookingForm
from . import db
import uuid

booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/events/<int:event_id>/book", methods=["GET", "POST"])
@login_required
def book_event(event_id):
    """Book tickets for an event (logged-in users only)."""
    event = db.session.get(Event, event_id)
    if event is None:
        flash("Event not found.", "danger")
        return redirect(url_for("event.list_events"))

    # Refresh status before allowing booking
    from .event import refresh_event_status
    refresh_event_status(event)
    db.session.commit()

    # Only allow booking for Open events with available tickets
    if event.status != EventStatus.OPEN:
        flash(f"This event is currently {event.status} and cannot be booked.", "warning")
        return redirect(url_for("event.event_detail", event_id=event_id))

    if event.available_tickets <= 0:
        flash("This event is sold out.", "warning")
        return redirect(url_for("event.event_detail", event_id=event_id))

    form = BookingForm()

    if request.method == "GET":
        # Set max quantity to available tickets
        form.quantity.render_kw = {"min": 1, "max": event.available_tickets}
        return render_template("booking/book.html", event=event, form=form)

    if form.validate_on_submit():
        quantity = form.quantity.data

        # Double-check available tickets (race condition guard)
        if quantity > event.available_tickets:
            flash(
                f"Only {event.available_tickets} tickets remaining. "
                f"Please reduce your quantity.",
                "danger",
            )
            return render_template("booking/book.html", event=event, form=form)

        # Create booking record
        order_id = str(uuid.uuid4())
        total_price = event.price * quantity

        booking = Booking(
            order_id=order_id,
            quantity=quantity,
            total_price=total_price,
            user_id=current_user.id,
            event_id=event.id,
        )
        db.session.add(booking)

        # Decrement available tickets
        event.available_tickets -= quantity

        # Auto-update status if sold out
        if event.available_tickets <= 0:
            event.status = EventStatus.SOLD_OUT

        db.session.commit()

        flash(f"Booking confirmed! Your Order ID is {order_id}", "success")
        return redirect(url_for("booking.booking_confirmation", booking_id=booking.id))

    return render_template("booking/book.html", event=event, form=form)


@booking_bp.route("/bookings/<int:booking_id>/confirmation")
@login_required
def booking_confirmation(booking_id):
    """Show booking confirmation page with Order ID."""
    booking = db.session.get(Booking, booking_id)
    if booking is None:
        flash("Booking not found.", "danger")
        return redirect(url_for("main.index"))

    # Only allow the booking owner to view
    if booking.user_id != current_user.id:
        flash("You can only view your own bookings.", "danger")
        return redirect(url_for("main.index"))

    return render_template("booking/confirmation.html", booking=booking)


@booking_bp.route("/my-bookings")
@login_required
def booking_history():
    """View booking history for the current user."""
    bookings = db.session.scalars(
        db.select(Booking)
        .where(Booking.user_id == current_user.id)
        .order_by(Booking.booking_date.desc())
    ).all()

    return render_template("booking/history.html", bookings=bookings)
