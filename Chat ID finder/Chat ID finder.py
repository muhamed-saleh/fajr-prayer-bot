import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load the .env file to get the token
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# This function will run every time a message is sent in the group
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    print("=========================================")
    print(f"SUCCESS! Your Group Chat ID is: {chat_id}")
    print("=========================================")
    print("You can now press Ctrl + C to stop this script.")
    print("Copy the number above into your .env file.")
    # We will make the application stop after finding the ID
    await application.stop()

# Main part of the script
if __name__ == '__main__':
    print("Starting ID Finder Bot...")
    print("Go to your Telegram group and send ANY message...")
    
    application = Application.builder().token(TOKEN).build()
    
    # This line tells the bot to run the message_handler function for any text message
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # This starts the bot
    application.run_polling()