# logger.py

from datetime import datetime

LOG_FILE = "auto_vpn.log"


def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"

    print(log_message)

    with open(LOG_FILE, "a") as f:
        f.write(log_message + "\n")
