from json import JSONDecodeError
import os

# Try to load .env file if it exists (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, will use environment variables directly
    pass

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

# Proxy configuration from environment variables
proxy_username = os.getenv("PROXY_USERNAME")
proxy_password = os.getenv("PROXY_PASSWORD")
proxy_host = os.getenv("PROXY_HOST")
proxy_port = os.getenv("PROXY_PORT")

proxies = None
if all([proxy_username, proxy_password, proxy_host, proxy_port]):
    proxy_url = f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }

# Retry logic: try up to 5 times
MAX_RETRIES = 5
status = "ERROR"

for attempt in range(1, MAX_RETRIES + 1):
    try:
        r = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        status = r.json()["is_online"]
        status = "ONLINE" if status else "OFFLINE"
        break  # Success, exit the retry loop
    except (JSONDecodeError, KeyError, requests.RequestException) as e:
        pass

# Get current time in Bangladesh timezone (Asia/Dhaka)
bd_timezone = pytz.timezone('Asia/Dhaka')
bd_time = datetime.now(bd_timezone)

# Define CSV file path
csv_file = "status.csv"

# Read existing entries from CSV
existing_entries = []
if os.path.exists(csv_file):
    try:
        with open(csv_file, "r", newline="") as f:
            reader = csv.reader(f)
            existing_entries = list(reader)
    except Exception as e:
        print(f"Warning: Could not read existing CSV file: {e}")
        existing_entries = []

# Keep only the last 95 entries (so with the new one, we'll have 96 total)
MAX_ENTRIES = 96
if len(existing_entries) >= MAX_ENTRIES:
    existing_entries = existing_entries[-(MAX_ENTRIES - 1):]

# Write back the existing entries plus the new one
try:
    with open(csv_file, "w", newline="") as f:
        w = csv.writer(f)
        # Write existing entries
        for entry in existing_entries:
            w.writerow(entry)
        # Write new entry
        w.writerow([bd_time.isoformat(), status])
    print(f"Status logged: {status} at {bd_time.isoformat()}")
except Exception as e:
    print(f"Error: Could not write to CSV file: {e}")
