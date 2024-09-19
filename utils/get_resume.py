import os

from .profile_data_fetcher import fetch_profile_data
from .resume_generator import generate_resume


def build_resume(
    linkedin_username, github_username, leetcode_username, filename="Resume.docx"
):
    os.makedirs(os.path.join("app", "resume"), exist_ok=True)
    profile_data = fetch_profile_data(
        linkedin_username, github_username, leetcode_username
    )
    generate_resume(profile_data, os.path.join("app", "resume", filename))


if __name__ == "__main__":
    build_resume("", "", "")
