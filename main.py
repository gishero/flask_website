from operator import truediv
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import time, timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "a;lsdkjf;alskdjf;alskdjf;alsdjf"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///logins.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class members(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")  # this sets the route to this page
# Defining the home page of our site
def home():
    return render_template("index.html")


# @app.route("/<name>/")
# def user(name):
#     return f"Hello {name}!"


@app.route("/test/")
def test():
    return render_template("test.html")


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash("Login Successful", "info")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in", "info")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email saved", "info")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))


@app.route("/logout/")
def logout():
    if "user" in session:
        user = session["user"]
        session.pop("user", None)
        session.pop("email", None)

    flash("Logged out", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
