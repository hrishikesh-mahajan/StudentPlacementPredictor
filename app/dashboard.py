import csv
import os

import joblib
import numpy as np
import pandas as pd
import requests
from flask import (
    Blueprint,
    g,
    make_response,
    redirect,
    render_template,
    send_from_directory,
)

from .auth import login_required
from .config import (
    get_csv_file_path,
    get_dashboard_embed_link_1,
    get_dashboard_embed_link_2,
    get_dashboard_embed_link_3,
    get_dashboard_link,
    get_google_form_link_ty,
    get_spreadsheet_link,
)
from utils.get_resume import build_resume

bp = Blueprint("dashboard", __name__)
ranges = {
    "None": 0,
    "1-50": 25,
    "50-150": 100,
    "150-300": 225,
    "300-500": 400,
    "500+": 500,
}
dsa_columns = [
    "DSA Questions Solved [Leetcode]",
    "DSA Questions Solved [HackerRank]",
    "DSA Questions Solved [GFG]",
    "DSA Questions Solved [Codechef]",
    "DSA Questions Solved [Codeforces]",
    "DSA Questions Solved [CodingNinjas]",
    "DSA Questions Solved [Other]",
]
columns = [
    "Medium of Schooling till 10th",
    "Branch",
    "Latest CGPA",
    "DSA Questions Solved [Aggregate]",
    "Participation Count [Industry Projects]",
    "Participation Count [Internships]",
    "Participation Count [Mini Projects]",
    "Participation Count [Hackathons]",
    "Club Affiliation [Technical Role]",
    "Club Affiliation [Non-Technical Role]",
]
weights = {
    "Medium of Schooling till 10th": 1,
    "Branch": 2,
    "Latest CGPA": 3,
    "DSA Questions Solved [Aggregate]": 20,
    "Participation Count [Industry Projects]": 5,
    "Participation Count [Internships]": 10,
    "Participation Count [Mini Projects]": 3,
    "Participation Count [Hackathons]": 4,
    "Club Affiliation [Technical Role]": 2,
    "Club Affiliation [Non-Technical Role]": 1,
}
mapping = {
    "Medium of Schooling till 10th": {},
    "Branch": {},
    "Latest CGPA": {},
    "DSA Questions Solved [Aggregate]": {},
    "Club Affiliation": {},
}
amcat_model = joblib.load(os.path.join("models", "amcat_model.pkl"))
amcat_scaler = joblib.load(os.path.join("models", "amcat_scaler.pkl"))
cocubes_model = joblib.load(os.path.join("models", "cocubes_model.pkl"))
cocubes_scaler = joblib.load(os.path.join("models", "cocubes_scaler.pkl"))


def get_user_dsa_score_sum(row):
    dsa_scores = [ranges.get(row[col], 0) for col in dsa_columns]
    return sum(dsa_scores)


def get_user_domain_score(user):
    score = 0
    cocubes_df = pd.read_csv(os.path.join("app", "cocubes_2025.csv"))
    if not cocubes_df.loc[cocubes_df["PRN"] == int(user["PRN"])].empty:
        score_1 = cocubes_df.loc[cocubes_df["PRN"] == int(user["PRN"])]
        score_1 = score_1.to_dict("records")[0]["Domain 1"]
        score_2 = cocubes_df.loc[cocubes_df["PRN"] == int(user["PRN"])]
        score_2 = score_2.to_dict("records")[0]["Domain 2"]
        score = (score_1 + score_2) / 2
    return score


def get_user_param_percentile(user, df, param_func):
    user_score = param_func(user)
    all_scores = [param_func(row) for _, row in df.iterrows()]
    return calculate_percentile(all_scores, user_score)


def predict_lpa(user):
    # Columns
    # Name,Branch,PRN,Automata,Logical Ability,English Comprehension,
    # Quantitative Ability
    if not isinstance(user, dict):
        user = user.to_dict()
    user_df = pd.DataFrame(user, index=[0])
    # Standardization
    user_data_scaled = amcat_scaler.transform(user_df)
    predicted_lpa = amcat_model.predict(user_data_scaled)[0]
    return predicted_lpa


def get_user_score(user):
    return predict_lpa(user)


def get_user_cocubes_score(user):
    if not isinstance(user, dict):
        user = user.to_dict()
    user_df = pd.DataFrame(user, index=[0])
    # Standardization
    user_data_scaled = cocubes_scaler.transform(user_df)
    predicted_lpa = cocubes_model.predict(user_data_scaled)[0]
    return predicted_lpa


def get_clean_link(url):
    if not url:
        return ""
    clean_url = url.split("?")[0]
    if not clean_url:
        return ""
    if clean_url[-1] == "/":
        return clean_url[:-1]
    return clean_url


def get_website_user_name(url):
    return url.split("/")[-1]


def get_user_info(user_id):
    # Columns
    # Timestamp,Email Address,Full Name,PRN,Medium of Schooling till 10th,
    # Branch,Latest CGPA,Programming Language Preference [1],
    # Programming Language Preference [2],Programming Language Preference [3],
    # Programming Language Preference [4],Programming Language Preference [5],
    # Programming Language Preference [6],Programming Language Preference [7],
    # DSA Questions Solved [Leetcode],DSA Questions Solved [HackerRank],
    # DSA Questions Solved [GFG],DSA Questions Solved [Codechef],
    # DSA Questions Solved [Codeforces],DSA Questions Solved [CodingNinjas],
    # DSA Questions Solved [Other],Participation Count [Industry Projects],
    # Participation Count [Internships],Participation Count [Mini Projects],
    # Participation Count [Hackathons],Club Affiliation [Technical Role],
    # Club Affiliation [Non-Technical Role],LinkedIn Profile Link,
    # LeetCode Profile Link,GitHub Profile Link,HackerRank Profile Link,
    # Unstop Profile Link
    user = {}
    found = False
    with open(get_csv_file_path(), "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if int(row["PRN"]) == user_id:
                found = True
                user = row
    if found:
        df = pd.read_csv(get_csv_file_path())
        user["LinkedIn"] = get_clean_link(user["LinkedIn Profile Link"])
        user["Developer"] = user["Development"] == "Yes"
        user["Full Name"] = get_user_name(user["Full Name"])
        if user["Developer"]:
            user["LeetCode"] = get_clean_link(user["LeetCode Profile Link"])
            user["GitHub"] = get_clean_link(user["GitHub Profile Link"])
            user["dsa_percentile"] = get_user_param_percentile(
                user, df, get_user_dsa_score_sum
            )
        else:
            user["LeetCode"] = ""
            user["GitHub"] = ""
            user["dsa_percentile"] = get_user_param_percentile(
                user, df, get_user_domain_score
            )
        user["cgpa_percentile"] = calculate_percentile(
            df["Latest CGPA"], user["Latest CGPA"]
        )
        user["percentile"] = get_user_percentile(user, df)
        user["grade"] = get_user_grade(user)
        for col in user.keys():
            if user[col] == "None":
                user[col] = 0
        return user
    return None


def get_user_name(full_name):
    name_list = full_name.split()
    if len(name_list) == 0:
        return ""
    elif len(name_list) == 1:
        return name_list[0]
    elif len(name_list) != 2:
        return str(name_list[0] + " " + name_list[-1])
    return full_name


def calculate_percentile(arr, number):
    sorted_arr = np.sort(arr)
    index = np.searchsorted(sorted_arr, number)
    percentile = (index / len(sorted_arr)) * 100
    return int(percentile)


def get_user_percentile(user, df):
    percentile = 50
    amcat_df = pd.read_csv(os.path.join("app", "amcat_2025.csv"))
    if not amcat_df.loc[amcat_df["PRN"] == int(user["PRN"])].empty:
        branch_mapping = {"Comp": 3, "IT": 2, "ENTC": 1}
        amcat_df["Branch"] = amcat_df["Branch"].map(branch_mapping)
        amcat_user = (
            amcat_df.loc[amcat_df["PRN"] == int(user["PRN"])]
            .drop(["Name", "PRN"], axis=1)
            .to_dict("records")[0]
        )
        amcat_df.drop(["Name", "PRN"], axis=1, inplace=True)
        percentile = get_user_param_percentile(amcat_user, amcat_df, get_user_score)
    if not user["Developer"]:
        cocubes_df = pd.read_csv(os.path.join("app", "cocubes_2025.csv"))
        if not cocubes_df.loc[cocubes_df["PRN"] == int(user["PRN"])].empty:
            cocubes_user = (
                cocubes_df.loc[cocubes_df["PRN"] == int(user["PRN"])]
                .drop(["Name", "PRN", "Branch"], axis=1)
                .to_dict("records")[0]
            )
            cocubes_df.drop(["Name", "PRN", "Branch"], axis=1, inplace=True)
            percentile = get_user_param_percentile(
                cocubes_user, cocubes_df, get_user_cocubes_score
            )
    return percentile


def get_user_grade(user):
    grade = "A"
    percentile = user["percentile"]
    if percentile < 75:
        grade = "B"
    if percentile < 50:
        grade = "C"
    if percentile < 25:
        grade = "D"
    return grade


@bp.route("/links")
def links():
    return render_template("index.html")


@bp.route("/")
def index():
    return redirect("/analysis")


@bp.route("/user-not-found")
def user_not_found():
    return render_template("dashboard/user_not_found.html")


@bp.route("/analysis")
@login_required
def analysis():
    user_id = int(g.user["username"])
    user = get_user_info(user_id)
    if not user:
        return redirect("/user-not-found")
    return render_template("dashboard/analysis.html", user=user)


@bp.route("/grades")
@login_required
def grades():
    user_id = int(g.user["username"])
    user = get_user_info(user_id)
    if not user:
        return redirect("/user-not-found")
    return render_template("dashboard/grades.html", user=user)


@bp.route("/dashboard")
@login_required
def dashboard():
    user_id = int(g.user["username"])
    user = get_user_info(user_id)
    if not user:
        return redirect("/user-not-found")
    return render_template(
        "dashboard/dashboard.html",
        user=user,
        DASHBOARD_LINK=get_dashboard_link(),
        DASHBOARD_LINK_EMBED_1=get_dashboard_embed_link_1(),
        DASHBOARD_LINK_EMBED_2=get_dashboard_embed_link_2(),
        DASHBOARD_LINK_EMBED_3=get_dashboard_embed_link_3(),
    )


@bp.route("/profile")
@login_required
def profile():
    user_id = int(g.user["username"])
    user = get_user_info(user_id)
    if not user:
        return redirect("/user-not-found")
    return render_template("dashboard/profile.html", user=user)


@bp.route("/form")
@login_required
def form():
    return redirect(get_google_form_link_ty())


@bp.route("/update")
@login_required
def update():
    response = requests.get(get_spreadsheet_link())
    with open(get_csv_file_path(), mode="wb") as file:
        file.write(response.content)
    clean_csv()
    return redirect("/")


@bp.route("/resume")
@login_required
def resume():
    user = get_user_info(int(g.user["username"])) or {}
    filename = f"{user['Full Name']} - Resume.docx"
    if user and user["LinkedIn"] and user["LeetCode"] and user["GitHub"]:
        build_resume(
            linkedin_username=user["LinkedIn"].split("/")[-1],
            github_username=user["GitHub"].split("/")[-1],
            leetcode_username=user["LeetCode"].split("/")[-1],
            filename=filename,
        )
        return send_from_directory("resume", filename, as_attachment=True)
    return "<h1>Missing LinkedIn, LeetCode or GitHub profile link.</h1>"


def clean_csv():
    with open(get_csv_file_path(), "r") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = []
        for row in reader:
            row["LinkedIn Profile Link"] = (
                get_clean_link(row["LinkedIn Profile Link"])
                if "linkedin.com/in/" in row["LinkedIn Profile Link"]
                else ""
            )
            row["LeetCode Profile Link"] = (
                get_clean_link(row["LeetCode Profile Link"])
                if "leetcode.com/" in row["LeetCode Profile Link"]
                else ""
            )
            row["GitHub Profile Link"] = (
                get_clean_link(row["GitHub Profile Link"])
                if "github.com/" in row["GitHub Profile Link"]
                else ""
            )
            row["HackerRank Profile Link"] = (
                get_clean_link(row["HackerRank Profile Link"])
                if "hackerrank.com/" in row["HackerRank Profile Link"]
                else ""
            )
            row["Unstop Profile Link"] = (
                get_clean_link(row["Unstop Profile Link"])
                if "unstop.com/u/" in row["Unstop Profile Link"]
                else ""
            )
            if not row["Development"]:
                row["Development"] = "Yes"
            rows.append(row)
    with open(get_csv_file_path(), "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=reader.fieldnames or [])
        writer.writeheader()
        writer.writerows(rows)


@bp.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")


@bp.route("/sw.js")
def service_worker():
    response = make_response(send_from_directory("static", "sw.js"))
    response.headers["Cache-Control"] = "no-cache"
    return response
