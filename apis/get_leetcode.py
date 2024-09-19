from leetcode_scraper import LeetcodeScraper
from pprint import pprint

scraper = LeetcodeScraper()
username = ""
profile_data = scraper.scrape_user_profile(username)

profile_data.pop("userContestRankingInfo")
profile_data.pop("recentAcSubmissions")
profile_data.pop("skillStats")
profile_data.pop("userProfileCalendar")
profile_data.pop("userBadges")

pprint(profile_data)
