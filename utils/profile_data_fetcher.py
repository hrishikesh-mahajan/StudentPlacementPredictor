import json
import os

from linkedin_api import Linkedin

from apis.gemini_api import ai_response
from apis.get_github import (
    fetch_collaborations,
    fetch_github_profile,
    fetch_repository_info,
)
from apis.leetcode_scraper import LeetcodeScraper

leetcode_scraper = LeetcodeScraper()

CREDENTIALS_FILE = os.path.join(os.getcwd(), "apis", "api_credentials.json")
with open(CREDENTIALS_FILE, "r") as json_file:
    CREDENTIALS = json.load(json_file)


def fetch_profile_data(linkedin_username, github_username, leetcode_username):

    # LeetCode
    print(f"LeetCode: {leetcode_username}")

    leetcode_profile_data = leetcode_scraper.scrape_user_profile(leetcode_username)

    if leetcode_profile_data:
        leetcode_profile_data.pop("userContestRankingInfo", None)
        leetcode_profile_data.pop("recentAcSubmissions", None)
        leetcode_profile_data.get("userProfileCalendar", None).get(
            "matchedUser", None
        ).get("userCalendar", None).pop("submissionCalendar", None)

    # LinkedIn
    print(f"LinkedIn: {linkedin_username}")

    linkedin_api = Linkedin(
        CREDENTIALS["LINKEDIN"]["USERNAME"], CREDENTIALS["LINKEDIN"]["PASSWORD"]
    )
    linkedin_profile_data = linkedin_api.get_profile(linkedin_username)

    linkedin_profile = {
        "Personal Info": {
            "Name": linkedin_profile_data["firstName"]
            + " "
            + linkedin_profile_data["lastName"],
            "Address": linkedin_profile_data["geoLocationName"],
        },
        "social_media": [
            {
                "linkedin": linkedin_username,
                "github": github_username,
                "leetcode": leetcode_username,
            }
        ],
        "Profile Summary": linkedin_profile_data.get("headline", "N/A"),
        "work_experience": linkedin_profile_data.get("experience", []),
        "certificates": linkedin_profile_data.get("certifications"),
        "education": linkedin_profile_data.get("education"),
    }

    # GitHub
    print(f"GitHub: {github_username}")

    github_access_token = CREDENTIALS["GITHUB"]["ACCESS_TOKEN"]
    github_profile_data = fetch_github_profile(github_username, github_access_token)
    repo_info = fetch_repository_info(github_username, github_access_token) or {}

    projects = []
    skills = []

    for idx, project in enumerate(repo_info):
        print(f"Project {idx + 1}/{len(repo_info)}: {project['name']}")
        if project["language"] != None:
            description = ai_response(
                "Generate a 30 words description for the project "
                + project["name"]
                + " having language used: "
                + project["language"]
            )
        else:
            description = ai_response(
                "Generate a 30 words description for the project " + project["name"]
            )
        project_info = {
            "Name": project["name"],
            "Language": project["language"],
            "Description": description,
        }
        projects.append(project_info)

        projectSkills = ai_response(
            f"generate a string of skills(comma separated) from project: {project['name']} having language used: {project['language']} and description: {description}. There should be atleast one skill."
        )

        if len(projectSkills) != 0:
            skills.append(projectSkills)

    if len(projects) != 0:
        about_me = ai_response(
            f"Considering name, language and description from {projects} generate a 30 words about me section for the resume of this particular student"
        )
    else:
        about_me = ai_response(
            f"Write a about me section for resume of a B.Tech student. In 30 words"
        )

    github_projects = {
        "Projects": projects,
        "collaborations": fetch_collaborations(github_username, github_access_token),
        "About_me": about_me,
        "Skills": skills,
    }

    # Merged Data
    merged_data = dict(leetcode_profile_data)
    merged_data.update(linkedin_profile)
    merged_data.update(github_projects)

    return merged_data
