from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary key means this is a unique value
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary key means this is a unique value
    email = db.Column(db.String(150), unique=True)  # must be unique email
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship("Note")
