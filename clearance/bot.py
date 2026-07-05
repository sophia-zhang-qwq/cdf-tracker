import requests
import time
import sqlite3
import os
from alert import send_telegram_alert

BOT_TOKEN = os.environ["BOT_TOKEN"]

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
            LIMIT 5
        """).fetchall()
    except sqlite3.OperationalError:
        row = None
    conn.close()

    return row

while True:
    r = requests.get(
        url + "/getUpdates",
        params={"offset": last_update_id + 1}).json()

    for update in r["result"]:
        last_update_id = update["update_id"]
        text = update["message"]["text"].lower()

        if "hi" in text or "sb" in text:
            latest = get_latest_message()

            if latest:
                text = "Recent 5 Alerts:\n\n"
                for alert_time, message in latest:
                    text += f"Latest Alert Time: {alert_time}\n{message}\n\n"
                send_telegram_alert(text)
            else:
                send_telegram_alert("No previous message")

    time.sleep(10)