from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = "somesecretkey"

    # Database configuration (SQLite)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sitedata.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialise extensions
    db.init_app(app)
    Bootstrap5(app)

    # Login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    # User loader (avoids circular import by importing inside function)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id == user_id))

    # Register Blueprints
    from . import views
    app.register_blueprint(views.main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    from . import event
    app.register_blueprint(event.event_bp)

    from . import booking
    app.register_blueprint(booking.booking_bp)

    # Create database tables on first run
    with app.app_context():
        db.create_all()

    # ============================================================
    #  Error handlers
    # ============================================================
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("403.html"), 403

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template("500.html"), 500

    @app.errorhandler(400)
    def bad_request(e):
        return render_template("400.html"), 400

    return app
