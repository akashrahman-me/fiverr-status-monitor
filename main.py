from json import JSONDecodeError

import requests
import csv
from datetime import datetime
import pytz

username = "akash_codespace"

url = f"https://www.fiverr.com/users/{username}/is_online"
headers = {
    "Referer": f"https://www.fiverr.com/{username}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}

r = requests.get(url, headers=headers)
status = "ERROR"

try:
    status = r.json()["is_online"]
    status = "ONLINE" if status else "OFFLINE"
except (JSONDecodeError, KeyError) as e:
    pass

# Get current time in Bangladesh timezone (Asia/Dhaka)
bd_timezone = pytz.timezone('Asia/Dhaka')
bd_time = datetime.now(bd_timezone)

with open("status.csv", "a", newline="") as f:
    w = csv.writer(f)
    w.writerow([bd_time.isoformat(), status])
