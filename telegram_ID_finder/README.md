# Telegram Chat ID Finder 🆔

A simple, command-line Python utility to quickly and reliably find the unique Chat ID of any Telegram group. This tool is perfect for developers and bot administrators who need a Chat ID to configure their bots.

---

## ## Features
* **Simple to Use:** Just run the script and send a message.
* **Reliable:** Gets the ID directly from the Telegram API.
* **Auto-Stop:** The script automatically shuts down after successfully finding an ID.
* **Secure:** Uses a `.env` file to keep your bot token private.

---

## ## Requirements
* Python 3.6+
* A Telegram Bot Token. You can get one from [@BotFather](https://t.me/BotFather).

---

## ## ⚙️ Setup Instructions
Follow these steps **one time** to set up the tool.

1.  **Create a Project Folder**
    Create a new folder on your computer for this tool (e.g., `id_finder`).

2.  **Add the Script and `.env` File**
    * Save the Python code provided below into a file named `find_id.py` inside your new folder.
    * In the same folder, create a new file named exactly `.env`.

3.  **Add Your Bot Token**
    Open the `.env` file and add your Telegram Bot Token. It should look like this:
    ```ini
    TELEGRAM_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u1234saken"
    ```

4.  **Set Up the Virtual Environment**
    Open a terminal in your project folder and run the following commands to create and activate a virtual environment.
    ```powershell
    # 1. Create the virtual environment folder
    python -m venv venv

    # 2. Activate it (for Windows PowerShell)
    .\venv\Scripts\activate
    ```
    *You'll know it's active when you see `(venv)` at the start of your terminal prompt.*

5.  **Install Libraries**
    With your virtual environment active, run this command to install the necessary Python libraries:
    ```powershell
    pip install python-telegram-bot python-dotenv
    ```

---

## ## 🚀 How to Use
Once setup is complete, you can follow these steps anytime you need to find a new group ID.

1.  **Add Your Bot to the Group**
    Go to your Telegram group and add the bot (whose token you put in the `.env` file) as a member.

2.  **Run the Script**
    Make sure your virtual environment is active in your terminal and run the script:
    ```powershell
    python find_id.py
    ```
    The terminal will show a message: `Waiting for a message...`

3.  **Send a Message**
    Go to your Telegram group and send **any message**.

4.  **Get the ID**
    Look back at your terminal. It will immediately print a success message containing the **Group Name** and the **Group Chat ID**. The script will then stop automatically.

---

## ## 🩺 Troubleshooting

* **Error:** `ModuleNotFoundError: No module named 'dotenv'`
    * **Cause:** Your virtual environment is not active, or the libraries were not installed.
    * **Solution:** Make sure you see `(venv)` at the start of your terminal prompt. If not, run `.\venv\Scripts\activate`. Then, run the `pip install` command again.

* **Error:** `telegram.error.InvalidToken`
    * **Cause:** The token in your `.env` file is missing, incorrect, or the file is named wrong.
    * **Solution:** Double-check that your file is named exactly `.env` (not `.env.txt`). Verify the key is `TELEGRAM_TOKEN` and that you have correctly pasted the entire token value from BotFather inside the quotes.

<br>

<details>
<summary>▶️ Click to view the `find_id.py` code</summary>

```python
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
```
</details>