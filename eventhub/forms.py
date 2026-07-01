from flask_wtf import FlaskForm
from wtforms.fields import (
    TextAreaField,
    SubmitField,
    StringField,
    PasswordField,
    IntegerField,
    DateTimeField,
    SelectField,
    FloatField,
)
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    NumberRange,
)


# ============================================================
#  Authentication forms
# ============================================================
class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[InputRequired("Enter email"), Email("Please enter a valid email")],
    )
    password = PasswordField(
        "Password", validators=[InputRequired("Enter password")]
    )
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    first_name = StringField(
        "First Name", validators=[InputRequired(), Length(max=64)]
    )
    last_name = StringField(
        "Last Name", validators=[InputRequired(), Length(max=64)]
    )
    email = StringField(
        "Email Address",
        validators=[InputRequired(), Email("Please enter a valid email"), Length(max=120)],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            EqualTo("confirm", message="Passwords should match"),
        ],
    )
    confirm = PasswordField("Confirm Password")
    phone = StringField(
        "Phone Number", validators=[InputRequired(), Length(max=20)]
    )
    street_address = StringField(
        "Street Address", validators=[InputRequired(), Length(max=255)]
    )
    submit = SubmitField("Register")


# ============================================================
#  Event forms
# ============================================================
class EventForm(FlaskForm):
    name = StringField(
        "Event Name", validators=[InputRequired(), Length(max=200)]
    )
    description = TextAreaField(
        "Description", validators=[InputRequired()]
    )
    category = SelectField(
        "Category",
        choices=[
            ("Conference", "Conference"),
            ("Workshop", "Workshop"),
            ("Social", "Social"),
            ("Music", "Music"),
            ("Sports", "Sports"),
            ("Other", "Other"),
        ],
        validators=[InputRequired()],
    )
    date = DateTimeField(
        "Date & Time", validators=[InputRequired()]
    )
    venue = StringField(
        "Venue", validators=[InputRequired(), Length(max=255)]
    )
    price = FloatField(
        "Ticket Price ($)",
        validators=[InputRequired(), NumberRange(min=0)],
    )
    total_tickets = IntegerField(
        "Total Tickets",
        validators=[InputRequired(), NumberRange(min=1)],
    )
    image = StringField(
        "Image URL (optional)", validators=[Length(max=500)]
    )
    submit = SubmitField("Create Event")


class CommentForm(FlaskForm):
    content = TextAreaField(
        "Your Comment", validators=[InputRequired(), Length(max=1000)]
    )
    submit = SubmitField("Post Comment")


# ============================================================
#  Booking form
# ============================================================
class BookingForm(FlaskForm):
    quantity = IntegerField(
        "Number of Tickets",
        validators=[InputRequired(), NumberRange(min=1, message="At least 1 ticket required")],
    )
    submit = SubmitField("Book Now")
