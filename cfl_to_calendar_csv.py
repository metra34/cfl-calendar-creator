import json
import csv
import os
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
import sys

# Load .env file if it exists
load_dotenv()

# Read file names from .env or use default
INPUT_FILE = os.getenv('INPUT_FILE', 'raw_schedule.json')
OUTPUT_FILE = os.getenv('OUTPUT_FILE', 'cfl_schedule.csv')

# Set your local timezone
LOCAL_TIMEZONE = pytz.timezone('America/Toronto')  # Adjust as needed

# Load the JSON
try:
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"🔴 File '{INPUT_FILE}' not found.")
    sys.exit(1)

# Prepare CSV output
csv_rows = []
csv_headers = [
    "Subject",
    "Start Date",
    "Start Time",
    "End Date",
    "End Time",
    "Description",
    "Location"
]

for week in data:
    if 'tournaments' not in week:
        continue
    for game in week['tournaments']:
        # Skip if no date or missing teams
        if 'date' not in game or not game.get('homeSquad') or not game.get('awaySquad'):
            continue

        try:
            # Parse UTC date
            utc_start = datetime.fromisoformat(game['date'].replace("Z", "+00:00"))
            local_start = utc_start.astimezone(LOCAL_TIMEZONE)
            local_end = local_start + timedelta(hours=3)

            # Game title
            if week.get("type") == "REG" or week.get("type") == "PRE":
                subject = f"{game['awaySquad']['name']} @ {game['homeSquad']['name']}"
            else:
                subject = week.get("name", "TBD @ TBD")

            csv_rows.append([
                subject,
                local_start.strftime("%Y-%m-%d"),
                local_start.strftime("%H:%M"),
                local_end.strftime("%Y-%m-%d"),
                local_end.strftime("%H:%M"),
                week.get("name", ""),
                ""
            ])
        except Exception as e:
            print(f"🟡 Skipping game due to error: {e}", file=sys.stderr)

# Write to CSV
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)
    writer.writerows(csv_rows)

print(f"🟢 CSV saved as '{OUTPUT_FILE}' with {len(csv_rows)} games.")
