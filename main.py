import os
import time
import schedule
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Bot

# --- Basic Setup ---
# 1. Load environment variables from the .env file
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 2. Configure logging to see the bot's activity
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# --- Core Bot Functionality ---
async def send_daily_poll():
    """This function creates and sends the poll."""
    try:
        bot = Bot(token=TOKEN)
        question = "☀️"
        options = ["صحيني", "صحيت الحمد لله"]

        logger.info(f"Sending poll to chat ID: {CHAT_ID}")
        await bot.send_poll(
            chat_id=CHAT_ID,
            question=question,
            options=options,
            is_anonymous=False,
            allows_multiple_answers=False
        )
        logger.info("Poll sent successfully!")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

def job():
    """Helper function to run the async poll sender."""
    logger.info("Scheduler triggered. Running the poll job.")
    asyncio.run(send_daily_poll())


# --- Scheduling ---
def start_scheduler():
    """Sets up and runs the scheduler."""
    # Set the time for the poll based on your local time.
    # "21:00" is 9 PM. "21:30" is 9:30 PM.
    schedule.every().day.at("20:30").do(job)
    logger.info("Scheduler started. Bot is now waiting for the scheduled time.")

    while True:
        schedule.run_pending()
        time.sleep(1)


# --- Main Execution ---
if __name__ == "__main__":
    if not TOKEN or not CHAT_ID:
        logger.error("TELEGRAM_TOKEN or CHAT_ID not found. Please check your .env file.")
    else:
        start_scheduler()