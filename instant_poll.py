import os
import logging
import asyncio
import datetime
import json  # <-- We need json to read the config file
from dotenv import load_dotenv
from telegram import Bot

# --- Basic Setup ---
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
# CHAT_IDS_STRING is no longer needed

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# --- Helper Function ---
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
async def send_poll_instantly(groups):
    """Sends the poll immediately to a list of group objects."""
    bot = Bot(token=TOKEN)
    today = datetime.date.today()
    arabic_months = {
        1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل", 5: "مايو", 6: "يونيو",
        7: "يوليو", 8: "أغسطس", 9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
    }
    date_str = f"{today.day} {arabic_months.get(today.month, '')} {today.year}"
    base_question = "صحيت؟"
    question = f"({date_str}) - {base_question}"
    options = ["صحيت الحمد لله", "لسا مصحيتش رن عليا"]
    
    for group in groups:
        chat_id = group.get('id')
        group_name = group.get('name', 'Unknown Group') # <-- Get the group name
        if not chat_id:
            continue

        try:
            # --- THIS IS THE UPDATED LOG MESSAGE ---
            logger.info(f"Instantly sending poll to '{group_name}' (ID: {chat_id})")
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
    logger.info("Instant Send script started by admin.")
    
    if not TOKEN:
        logger.error("TELEGRAM_TOKEN not found in .env file.")
    else:
        # Load groups from the JSON file instead of the old string
        groups_to_poll = load_groups_from_config()
        if not groups_to_poll:
            logger.warning("No groups found in config.json. Exiting.")
        else:
            asyncio.run(send_poll_instantly(groups_to_poll))
                
    logger.info("Instant Send script finished.")