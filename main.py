import json
import time
from datetime import datetime

import requests

ENABLE_TELEGRAM = False
TELEGRAM_CHAT_ID = 0
UNIVERSE_ID = 0
PLACE_ID = 0
PLACE_NAME = "some name [{}]"

URL = f"https://apis.roblox.com/legacy-badges/v1/universes/{UNIVERSE_ID}/badges"

with open("telegram_token.txt", "r") as telegram_token_file:
    telegram_token = telegram_token_file.read().strip()


with open("robloxtoken.txt", "r") as roblox_token_file:
    roblox_token = roblox_token_file.read().strip()


with open("badgeno.json", "r") as badgeno_file:
    badgeno = json.load(badgeno_file)


def send_message(message):
    if not ENABLE_TELEGRAM:
        return
    requests.post(f"https://api.telegram.org/bot{telegram_token}/sendMessage", params={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"[badgeCreator] {message}"
    })


def append_badge_log(badge_name: str):
    with open("badge_logs.txt", "a") as badge_logs_file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        badge_logs_file.write(f"{current_time} - {badge_name}\n")


if __name__ == '__main__':
    session = requests.Session()
    session.headers.update({
        "x-api-key": roblox_token
    })
    for i in range(5):
        closed = False
        files = {
            "file": (f"icon_{i}.png", open("badge.png", "rb"), "image/png")
        }
        data = {
            "name": f"free badge {badgeno['free_badges']}",
            "description": f"free badge {badgeno['free_badges']}",
            "paymentSourceType": 1,
            "expectedCost": 0
        }
        fails_500 = 0
        while True:
            response = session.post(URL, data=data, files=files)
            if not closed:
                closed = True
                files["file"][1].close()

            print(response.status_code)
            print(response.text)
            print("loop", i, fails_500)

            if response.status_code == 200:
                badgeno["free_badges"] += 1
                badgeno["current_badge"] += 1
                if badgeno["current_badge"] % 100 == 0:
                    send_message(f"Created {badgeno['current_badge']} badges")
                append_badge_log(data["name"])
                break
            elif response.status_code == 500:
                fails_500 += 1
                time.sleep(25)
                if fails_500 == 15:
                    send_message(f"Error on 500 creating badge: {fails_500} | {response.status_code} | {response.text} | {badgeno['free_badges']} | {badgeno['current_badge']} | {i}")
                    break
            else:
                send_message(f"Error on creating badge: {response.status_code} | {response.text} | {badgeno['free_badges']} | {badgeno['current_badge']} | {i}")
                break

        time.sleep(10)

    with open("badgeno.json", "w") as badgeno_file:
        json.dump(badgeno, badgeno_file, indent=4)

    # Update place

    info_response = session.patch(
        f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/places/{PLACE_ID}?updateMask=displayName",
        json={
            "displayName": PLACE_NAME.format(str(badgeno["current_badge"]))
        }
    )

    if info_response.status_code != 200:
        send_message(f"Error on updating place: {info_response.status_code} | {info_response.text} | {badgeno['free_badges']} | {badgeno['current_badge']}")

    print(info_response.status_code)
    print(info_response.text)
