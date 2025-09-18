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
def get_fajr_time(city, country):
    """Fetches Fajr prayer time from the aladhan.com API."""
    try:
        url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=5"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['data']['timings']['Fajr']
    except Exception as e:
        logger.error(f"Failed to get prayer times: {e}")
        return None

def load_groups_from_config():
    """Loads the list of groups from the config.json file."""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            return config_data.get('groups', [])
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error("config.json file not found or is empty/invalid.")
        return []

# --- Core Bot Functionality ---
async def send_poll_to_groups(groups):
    """Sends the poll with the new default content to a list of group objects."""
    bot = Bot(token=TOKEN)
    today = datetime.date.today()
    arabic_months = {
        1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل", 5: "مايو", 6: "يونيو",
        7: "يوليو", 8: "أغسطس", 9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
    }
    date_str = f"{today.day} {arabic_months.get(today.month, '')} {today.year}"
    
    # --- Your new default poll details ---
    base_question = "صحيت؟"
    question = f"({date_str}) - {base_question}"
    options = ["صحيت الحمد لله", "لسا مصحيتش رن عليا"]
    
    for group in groups:
        chat_id = group.get('id')
        group_name = group.get('name', 'Unknown Group')
        if not chat_id:
            continue

        try:
            logger.info(f"Sending poll to '{group_name}' (ID: {chat_id})")
            await bot.send_poll(
                chat_id=chat_id, question=question, options=options,
                is_anonymous=False, allows_multiple_answers=False
            )
            logger.info(f"Poll sent successfully to '{group_name}'!")
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Failed to send poll to '{group_name}'. Error: {e}")

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
            fajr_time = get_fajr_time(city="Mansoura", country="Egypt")
            if fajr_time:
                EEST = datetime.timezone(datetime.timedelta(hours=3))
                now_egypt = datetime.datetime.now(EEST)
                fajr_hour, fajr_minute = map(int, fajr_time.split(':'))
                fajr_datetime = now_egypt.replace(hour=fajr_hour, minute=fajr_minute, second=0, microsecond=0)
                poll_time = fajr_datetime - datetime.timedelta(hours=1)
                wait_seconds = (poll_time - now_egypt).total_seconds()
                
                if wait_seconds > 0:
                    logger.info(f"Waiting for {wait_seconds / 60:.2f} minutes.")
                    time.sleep(wait_seconds)
                    logger.info("It's time! Sending polls...")
                    asyncio.run(send_poll_to_groups(groups_to_poll))
                else:
                    logger.info("Poll time has already passed for today.")
                    
    logger.info("Script finished.")