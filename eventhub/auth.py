from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration page."""
    form = RegisterForm()
    if form.validate_on_submit():
        # Check email uniqueness
        existing = db.session.scalar(
            db.select(User).where(User.email == form.email.data)
        )
        if existing:
            flash("An account with this email already exists.", "danger")
            return render_template("user.html", form=form, heading="Register")

        # Hash password and create user
        pw_hash = generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password_hash=pw_hash,
            phone=form.phone.data,
            street_address=form.street_address.data,
        )
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("user.html", form=form, heading="Register")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login page."""
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(User.email == form.email.data)
        )
        if user is None:
            flash("No account found with that email.", "danger")
        elif not check_password_hash(user.password_hash, form.password.data):
            flash("Incorrect password.", "danger")
        else:
            login_user(user)
            flash(f"Welcome back, {user.first_name}!", "success")
            next_page = request.args.get("next")
            if not next_page or not next_page.startswith("/"):
                next_page = url_for("main.index")
            return redirect(next_page)

    return render_template("user.html", form=form, heading="Login")


@auth_bp.route("/logout")
@login_required
def logout():
    """Log the user out."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))
