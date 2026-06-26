import requests
import time
import sqlite3

from alert import send_telegram_alert

BOT_TOKEN = "8751194675:AAE7HweS5jFFhDm4HUCBsB_2ulOTzKfL3Nc"

url = f"https://api.telegram.org/bot{BOT_TOKEN}"

last_update_id = 0

DB = "clearance.db"

def get_latest_message():

    conn = sqlite3.connect(DB)

    try:
        row = conn.execute("""
            SELECT time, message
            FROM messages
            ORDER BY id DESC
            LIMIT 1
        """).fetchone()
    except sqlite3.OperationalError:
        row = None

    conn.close()

    return row

while True:

    r = requests.get(
        url + "/getUpdates",
        params={
            "offset": last_update_id + 1
        }
    ).json()

    for update in r["result"]:

        last_update_id = update["update_id"]

        text = update["message"]["text"].lower()

        if "hi" in text or "sb" in text:
            latest = get_latest_message()

            if latest:
                time,message = latest
                send_telegram_alert( f"""Latest Alert Time: {time} {message} """ )
            else:
                send_telegram_alert("No previous message")

    time.sleep(10)