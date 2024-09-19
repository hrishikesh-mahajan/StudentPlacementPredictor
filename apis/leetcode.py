import csv
import os

from leetcode_scraper import LeetcodeScraper

scraper = LeetcodeScraper()


def get_leetcode_data(username):
    profile_data = scraper.scrape_user_profile(username)
    languageStats = profile_data.get("languageStats") or {}
    matchedUser = languageStats.get("matchedUser") or {}
    languageProblemCount = matchedUser.get("languageProblemCount") or []
    if languageProblemCount:
        result = languageProblemCount[0]
        result["username"] = username
        print(result)
        return result
    return None


profile_csv = os.path.join("apis", "leetcode_profiles.csv")


def get_student_data():
    with open(os.path.join("app", "students.csv"), "r") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = []
        for row in reader:
            if not row["LeetCode Profile Link"]:
                continue
            username = row["LeetCode Profile Link"].split("/")[-1]
            result_row = get_leetcode_data(username) or {}
            if result_row and result_row.get("problemsSolved", 0) > 0:
                result_row["PRN"] = row["PRN"]
                rows.append(result_row)

    with open(profile_csv, "w", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=["PRN", "username", "languageName", "problemsSolved"]
        )
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    get_student_data()
