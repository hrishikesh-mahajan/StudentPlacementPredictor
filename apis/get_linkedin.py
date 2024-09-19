import json
import os
import pprint

from linkedin_api import Linkedin

CREDENTIALS_FILE = os.path.join(os.getcwd(), "apis", "api_credentials.json")
with open(CREDENTIALS_FILE, "r") as json_file:
    CREDENTIALS = json.load(json_file)

    api = Linkedin(
        CREDENTIALS["LINKEDIN"]["USERNAME"], CREDENTIALS["LINKEDIN"]["PASSWORD"]
    )

    profile_username = input("Enter Username: ")
    profile_data = api.get_profile(profile_username)
    pprint.pprint(profile_data)
