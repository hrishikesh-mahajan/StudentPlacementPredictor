import json
import os
import random
import time

import google.generativeai as genai

CREDENTIALS_FILE = os.path.join(os.getcwd(), "apis", "api_credentials.json")

with open(CREDENTIALS_FILE, "r") as json_file:
    CREDENTIALS = json.load(json_file)

    API_KEY = CREDENTIALS["GEMINI"]["API_KEY"]


genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-pro")

streak = 0


def ai_response(prompt, delay=0):
    global streak
    try:
        response = model.generate_content(prompt)
        if delay:
            print()
            print("API Cooldown:", delay, "seconds")
        streak += 1
        return response.text
    except:
        print(".", end="")
        time.sleep(1)
        streak = 0
        return ai_response(prompt, delay=delay + 1)


def main():
    prompt = "Hello, world!"
    promptNumber = 1
    response = ""
    MAX_PROMPTS = 100
    maxStreak = 0
    while promptNumber <= MAX_PROMPTS:
        print("Prompt:", promptNumber)
        response = ai_response(prompt)
        print("Streak:", streak)
        if streak > maxStreak:
            maxStreak = streak
        promptNumber += 1
    print("Max Streak:", maxStreak)
    print(response)


if __name__ == "__main__":
    main()
