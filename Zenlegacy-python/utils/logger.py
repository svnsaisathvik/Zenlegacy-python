import os
from datetime import datetime

LOG_FILE_PATH = "logs/action_logs.txt"

def log_action(action_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {action_message}\n"

    # Ensure the logs directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Append the log entry to the action log file
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(log_entry)
