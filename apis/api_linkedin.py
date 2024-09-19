from linkedin_api import Linkedin

api = Linkedin("", "")

profile_username = input("input your username: ")
profile_data = api.get_profile(profile_username)

print("Name:", profile_data["firstName"], profile_data["lastName"])
print("Headline:", profile_data.get("headline", "N/A"))
print("Location:", profile_data.get("location", {}).get("name", "N/A"))
print("Summary:", profile_data.get("summary", "N/A"))
print("Skills:", ", ".join(skill["name"] for skill in profile_data.get("skills", [])))
print("Experience:")
for experience in profile_data.get("experience", []):
    print(
        f"- {experience.get('title', 'N/A')} \
            at {experience.get('companyName', 'N/A')}"
    )
