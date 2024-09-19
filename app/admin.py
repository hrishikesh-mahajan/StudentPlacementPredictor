import json

import pandas as pd
import requests
from flask import Blueprint, redirect, render_template, request

from .auth_admin import admin_login_required
from .config import CONFIG_FILE, get_csv_file_path, get_spreadsheet_link
from .send_emails import send_email_to_everyone, send_email_to_selected

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=("GET", "POST"))
@admin_login_required
def admin_dashboard():
    with open(CONFIG_FILE, "r") as json_file:
        CURRENT_CONFIG = json.load(json_file)
    if request.method == "POST":
        with open(CONFIG_FILE, "r") as json_file:
            NEW_CONFIG = json.load(json_file)
            for val in request.form.keys():
                NEW_CONFIG[val] = request.form[val]
        with open(CONFIG_FILE, "w") as json_file:
            json.dump(NEW_CONFIG, json_file, indent=2)
        return redirect("/admin")
    return render_template("admin/admin_dashboard.html", CURRENT_CONFIG=CURRENT_CONFIG)


@bp.route("/gform", methods=("GET", "POST"))
@admin_login_required
def admin_gform():
    with open(CONFIG_FILE, "r") as json_file:
        CURRENT_CONFIG = json.load(json_file)
    if request.method == "POST":
        with open(CONFIG_FILE, "r") as json_file:
            NEW_CONFIG = json.load(json_file)
            for val in request.form.keys():
                NEW_CONFIG[val] = request.form[val]
        with open(CONFIG_FILE, "w") as json_file:
            json.dump(NEW_CONFIG, json_file, indent=2)
        return redirect("/admin/gform")
    return render_template("admin/admin_gform.html", CURRENT_CONFIG=CURRENT_CONFIG)


@bp.route("/email", methods=("GET", "POST"))
@admin_login_required
def admin_email():
    df = pd.read_csv(get_csv_file_path())
    with open(CONFIG_FILE, "r") as json_file:
        CURRENT_CONFIG = json.load(json_file)
    if request.method == "POST":
        email_list = [
            key for key in request.form.keys() if request.form[key] == "send_email"
        ]
        send_email_to_selected(email_list)
    return render_template(
        "admin/admin_email.html",
        email_list=df["Email Address"],
        CURRENT_CONFIG=CURRENT_CONFIG,
    )


@bp.route("/email-send", methods=("GET", "POST"))
@admin_login_required
def admin_email_send():
    send_email_to_everyone()
    return redirect("/admin/email")


@bp.route("/update")
@admin_login_required
def update():
    response = requests.get(get_spreadsheet_link())
    with open(get_csv_file_path(), mode="wb") as file:
        file.write(response.content)
    return redirect("/admin")
