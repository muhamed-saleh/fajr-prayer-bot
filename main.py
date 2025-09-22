import os
import logging
import asyncio
import datetime
import requests
import time
import json
from dotenv import load_dotenv
from telegram import Bot

# --- Basic Setup ---
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Helper Functions ---
def get_fajr_time(city, country, for_date=None):
    """Fetches Fajr prayer time for a specific date if provided."""
    try:
        date_str = for_date.strftime("%d-%m-%Y") if for_date else ""
        url = f"http://api.aladhan.com/v1/timingsByCity/{date_str}?city={city}&country={country}&method=5"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        fajr_time = data['data']['timings']['Fajr']
        logger.info(f"Successfully fetched Fajr time for {city} on {for_date.strftime('%Y-%m-%d')}: {fajr_time}")
        return fajr_time
    except Exception as e:
        logger.error(f"Failed to get prayer times: {e}")
        return None

def load_groups_from_config():
    """Loads the list of groups from the config.json file."""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('groups', [])
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error("config.json file not found or is empty/invalid.")
        return []

# --- Core Bot Functionality ---
async def send_poll_to_groups(groups):
    # This function is the same as before, no changes needed here.
    # ...

# --- Main Execution ---
if __name__ == "__main__":
    logger.info("Daily script started.")
    
    if not TOKEN:
        logger.error("TELEGRAM_TOKEN not found in .env file.")
    else:
        groups_to_poll = load_groups_from_config()
        if not groups_to_poll:
            logger.warning("No groups found in config.json. Exiting.")
        else:
            EEST = datetime.timezone(datetime.timedelta(hours=3))
            now_egypt = datetime.datetime.now(EEST)
            
            # --- NEW LOGIC TO CHECK TODAY AND TOMORROW ---
            
            # 1. First, check for today's time
            fajr_time_today = get_fajr_time(city="Mansoura", country="Egypt", for_date=now_egypt.date())
            
            if fajr_time_today:
                fajr_hour, fajr_minute = map(int, fajr_time_today.split(':'))
                fajr_datetime_today = now_egypt.replace(hour=fajr_hour, minute=fajr_minute, second=0, microsecond=0)
                poll_time = fajr_datetime_today - datetime.timedelta(hours=1)
                
                wait_seconds = (poll_time - now_egypt).total_seconds()
                
                # 2. If today's time has passed, calculate for tomorrow
                if wait_seconds < 0:
                    logger.info("Poll time for today has passed. Calculating wait time for tomorrow's Fajr.")
                    tomorrow_date = now_egypt.date() + datetime.timedelta(days=1)
                    fajr_time_tomorrow = get_fajr_time(city="Mansoura", country="Egypt", for_date=tomorrow_date)
                    
                    if fajr_time_tomorrow:
                        fajr_hour, fajr_minute = map(int, fajr_time_tomorrow.split(':'))
                        tomorrow_datetime = datetime.datetime(
                            year=tomorrow_date.year, month=tomorrow_date.month, day=tomorrow_date.day,
                            hour=fajr_hour, minute=fajr_minute, tzinfo=EEST
                        )
                        poll_time = tomorrow_datetime - datetime.timedelta(hours=1)
                        wait_seconds = (poll_time - now_egypt).total_seconds()

                # 3. Now, wait for the calculated duration (either for today or tomorrow)
                if wait_seconds > 0:
                    logger.info(f"Current Egypt time: {now_egypt.strftime('%H:%M')}. Next poll at: {poll_time.strftime('%Y-%m-%d %H:%M')}.")
                    logger.info(f"Waiting for {wait_seconds / 3600:.2f} hours.")
                    time.sleep(wait_seconds)
                    
                    logger.info("It's time! Sending polls...")
                    asyncio.run(send_poll_to_groups(groups_to_poll))
                else:
                    logger.error("Could not calculate a future poll time. Exiting.")
            
    logger.info("Script finished.")