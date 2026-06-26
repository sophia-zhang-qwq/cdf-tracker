# test for telegram bot
import requests
from datetime import datetime
from email.mime.text import MIMEText
import smtplib
import sqlite3

# Telegram credentials
BOT_TOKEN = "8751194675:AAE7HweS5jFFhDm4HUCBsB_2ulOTzKfL3Nc"
CHAT_ID = "8916177069"

# Email credentials
sender_email = "qwqsophiazhang@gmail.com"
receiver_email = ["wenminqizhang@gmail.com", "qwqsophiazhang@gmail.com"]
# TODO： Hide password before post to Github
 # cijb abqm cifs yhzx
email_password = "cijbabqmcifsyhzx"

# last message
def save_message(message):

    conn = sqlite3.connect("clearance.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            message TEXT
        )
    """)

    conn.execute("""
        INSERT INTO messages(time,message)
        VALUES(datetime('now','localtime'),?)
    """,(message,))

    conn.commit()
    conn.close()


def send_telegram_alert(message):
    global LAST_MESSAGE

    LAST_MESSAGE = message
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text":
                f"🚨 Clearance Alert\n"
                f"Time: {current_time}\n\n"
                f"{message}"
        }
    )
    print("Telegram Alert Sent.")

# sender_email,receiver_email,email_password
def send_email_alert(message):
    msg = MIMEText(message)

    msg["Subject"] = "Alpha Detected in Clearance"
    msg["From"] =  sender_email
    # To >1 email address
    #msg["To"] = receiver_email
    msg["To"] = ", ".join(receiver_email)

    server = smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    )

    server.login(
        sender_email,
        email_password
    )

    server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)
    print("Email Sent.")
    server.quit()


def send_alert(message):
    save_message(message)
    send_telegram_alert(message)
    send_email_alert(message)


# test
if __name__ == "__main__":
    send_telegram_alert("Test Alert")

