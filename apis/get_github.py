import json
import os
import pprint

import requests


def fetch_github_profile(username, access_token):
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching GitHub profile:", response.text)
        return None


def fetch_github_repositories(repos_url, access_token):
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(repos_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching GitHub repositories:", response.text)
        return None


def fetch_repository_info(username, access_token):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching repository information:", response.text)
        return None


def fetch_commit_activity(username, repository_name, access_token):
    url = f"https://api.github.com/repos/{username}/{repository_name}/commits"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return len(response.json())  # Count total commits
    else:
        print(
            f"Error fetching commit activity for repository \
                {repository_name}:",
            response.text,
        )
        return 0


def fetch_collaborations(username, access_token):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        collaborations = []
        for repo in repos:
            if repo["permissions"]["push"]:
                collaborations.append(repo["name"])
        return collaborations
    else:
        print("Error fetching collaborations:", response.text)
        return []


if __name__ == "__main__":
    github_username = input("Input the GitHub username: ")

    github_access_token = ""

    CREDENTIALS_FILE = os.path.join(os.getcwd(), "apis", "api_credentials.json")
    with open(CREDENTIALS_FILE, "r") as json_file:
        CREDENTIALS = json.load(json_file)
        github_access_token = CREDENTIALS["GITHUB"]["ACCESS_TOKEN"]

    profile_data = fetch_github_profile(github_username, github_access_token)

    if profile_data:
        pprint.pprint(profile_data)

        repos_url = profile_data["repos_url"]
        repositories = fetch_github_repositories(repos_url, github_access_token)
        pprint.pprint(repositories)

        repositories = fetch_repository_info(github_username, github_access_token)
        pprint.pprint(repositories)

        collaborations = fetch_collaborations(github_username, github_access_token)
        pprint.pprint(collaborations)
