import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- Setup ---
# Load the .env file to get the bot token
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


# --- Core Function ---
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function runs when a message is received. It prints the Chat ID and then stops the bot.
    """
    chat_id = update.message.chat.id
    chat_title = update.message.chat.title

    print("\n=========================================")
    print("           SUCCESS! ID FOUND             ")
    print("=========================================")
    print(f"Group Name: {chat_title}")
    print(f"Group Chat ID: {chat_id}")
    print("=========================================")
    print("You can now use this ID in your other bot projects.")
    
    # This tells the application to stop running once the ID is found.
    asyncio.create_task(context.application.stop())


# --- Main Execution ---
if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN not found. Please check your .env file.")
    else:
        print("Starting ID Finder Bot...")
        print("1. Make sure this bot is a member of your target group.")
        print("2. Go to your Telegram group now and send ANY message...")
        print("Waiting for a message...")

        application = Application.builder().token(TOKEN).build()
        
        # This handler will trigger the message_handler function for any text message
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

        # This starts the bot and waits for messages
        application.run_polling()
        
        print("\nBot has shut down gracefully.")