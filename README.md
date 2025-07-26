# cfl-calendar-creator

Convert raw JSON schedule data into a CSV that can be imported in google calendar

## Usage

1. Fetch the raw JSON data from the CFL API e.g. (https://www.cfl.ca/schedule/2025/)
   I used this link to raw data: https://cflscoreboard.cfl.ca/json/scoreboard/rounds.json
2. Save the JSON file as `raw_schedule.json` or set the `INPUT_FILE` environment variable
   - optionally set the `OUTPUT_FILE` environment variable to change the output file name
3. Run the script: `python cfl_to_calendar_csv.py`
4. Go to Google Calendar and import the CSV file

## Requirements

- Python 3.10+
- Python packages:
  - `python-dotenv`
  - `pytz`

## Environment Variables

- `INPUT_FILE`: Path to the raw JSON file. Default: `raw_schedule.json`
- `OUTPUT_FILE`: Path to the output CSV file. Default: `cfl_schedule.csv`
