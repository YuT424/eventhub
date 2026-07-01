from flask import Blueprint, render_template, request
from datetime import datetime
from .models import Event, EventStatus
from . import db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Landing page - displays upcoming events and categories."""
    search_query = request.args.get("search", "", type=str).strip()

    # Show upcoming Open events, ordered by date
    query = (
        db.select(Event)
        .where(Event.status == EventStatus.OPEN)
        .order_by(Event.date.asc())
    )

    if search_query:
        query = query.where(Event.name.ilike(f"%{search_query}%"))

    upcoming = db.session.scalars(query.limit(6)).all()

    categories = ["Conference", "Workshop", "Social", "Music", "Sports", "Other"]

    return render_template(
        "index.html",
        upcoming=upcoming,
        categories=categories,
        EventStatus=EventStatus,
        search_query=search_query,
    )
