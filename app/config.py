import json
import os

CONFIG_FILE = os.path.join(os.getcwd(), "app", "config.json")
with open(CONFIG_FILE, "r") as json_file:
    CURRENT_CONFIG = json.load(json_file)


def get_csv_filename():
    with open(CONFIG_FILE, "r") as json_file:
        CURRENT_CONFIG = json.load(json_file)
    return CURRENT_CONFIG["CSV_FILE"]


def get_csv_file_path():
    return os.path.join(os.getcwd(), "app", get_csv_filename())


def get_google_form_link_fy():
    with open(CONFIG_FILE, "r") as json_file:
        CURRENT_CONFIG = json.load(json_file)
    return CURRENT_CONFIG["GOOGLE_FORM_LINK_FY"]


def get_google_form_link_sy():
    with open(CONFIG_FILE, "r") as json_file:
        CURRENT_CONFIG = json.load(json_file)
    return CURRENT_CONFIG["GOOGLE_FORM_LINK_SY"]


def get_google_form_link_ty():
    with open(CONFIG_FILE, "r") as json_file:
        CURRENT_CONFIG = json.load(json_file)
    return CURRENT_CONFIG["GOOGLE_FORM_LINK_TY"]


def get_google_form_link_btech():
    with open(CONFIG_FILE, "r") as json_file:
        CURRENT_CONFIG = json.load(json_file)
    return CURRENT_CONFIG["GOOGLE_FORM_LINK_BTECH"]


def get_spreadsheet_id_ty():
    with open(CONFIG_FILE, "r") as json_file:
        CURRENT_CONFIG = json.load(json_file)
    return CURRENT_CONFIG["SPREADSHEET_ID_TY"]


def get_spreadsheet_link():
    return (
        "https://docs.google.com/spreadsheets/d/"
        + get_spreadsheet_id_ty()
        + "/export?format=csv"
    )


def get_dashboard_link():
    with open(CONFIG_FILE, "r") as json_file:
        CURRENT_CONFIG = json.load(json_file)
    return CURRENT_CONFIG["DASHBOARD_LINK"]


def get_dashboard_embed_link_1():
    with open(CONFIG_FILE, "r") as json_file:
        CURRENT_CONFIG = json.load(json_file)
    return CURRENT_CONFIG["DASHBOARD_LINK_EMBED_1"]


def get_dashboard_embed_link_2():
    with open(CONFIG_FILE, "r") as json_file:
        CURRENT_CONFIG = json.load(json_file)
    return CURRENT_CONFIG["DASHBOARD_LINK_EMBED_2"]


def get_dashboard_embed_link_3():
    with open(CONFIG_FILE, "r") as json_file:
        CURRENT_CONFIG = json.load(json_file)
    return CURRENT_CONFIG["DASHBOARD_LINK_EMBED_3"]
