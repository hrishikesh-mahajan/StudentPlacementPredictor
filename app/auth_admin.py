import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db as get_db_admin

bp = Blueprint("auth_admin", __name__, url_prefix="/auth-admin")


def admin_login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("/auth-admin/login")
        if not g.user["isAdmin"]:
            # error = (f"{g.user['username']} is not Admin User. "
            #          "Re-login as Admin. "
            #          "Current user has been logged out.")
            # flash(error)
            return redirect("/auth-admin/logout")
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_admin():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db_admin()
            .execute("SELECT * FROM user WHERE id = ?", (user_id,))
            .fetchone()
        )


@bp.route("/register", methods=("GET", "POST"))
def register_admin():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isAdmin = 1
        db = get_db_admin()
        error = None
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, isAdmin)" "VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), isAdmin),
                )
                db.commit()
            except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {username} is already registered."
            else:
                # Success, go to the login page.
                return redirect("/auth-admin/login")
        flash(error)
    return render_template("admin/admin_register.html")


@bp.route("/login", methods=("GET", "POST"))
def login_admin():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db_admin()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."
        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect("/admin")
        flash(error)
    return render_template("admin/admin_login.html")


@bp.route("/logout")
def logout_admin():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect("/admin")
