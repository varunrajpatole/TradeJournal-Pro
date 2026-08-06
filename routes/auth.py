from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from models import db
from models.user import User

from forms.login_form import LoginForm
from forms.register_form import RegisterForm

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(username=form.username.data).first()

        if existing_user:
            flash("Username already exists!", "danger")
            return redirect(url_for("auth.register"))

        existing_email = User.query.filter_by(email=form.email.data).first()

        if existing_email:
            flash("Email already exists!", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(form.password.data)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful!", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):

            login_user(user)

            return redirect(url_for("dashboard.dashboard"))

        flash("Invalid Username or Password", "danger")

    return render_template("login.html", form=form)


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("auth.login"))