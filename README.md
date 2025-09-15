# Telegram Daily Poll Bot

A simple, scalable Python bot that automatically sends a daily poll with a dynamic date as the question to one or more Telegram groups at a scheduled time.

This project was built to be deployed on a service like PythonAnywhere for 24/7 operation.

---

## ## Features

- **Daily Automation:** Sends a poll at a specific time every day.
- **Dynamic Content:** The poll question is automatically set to the current date.
- **Scalable:** Can send the same poll to multiple groups by listing their IDs.
- **Efficient:** The code is optimized to run as a scheduled task, making it suitable for free hosting services.
- **Utility Included:** Comes with a helper script (`find_id.py`) to easily find group Chat IDs.

---

## ## ⚙️ Setup Instructions

1.  **Get a Bot Token:**
    - Talk to the [@BotFather](https://t.me/BotFather) on Telegram to create a new bot and get its API token.
    - Disable group privacy for your bot via BotFather's settings so it can be added to groups.

2.  **Clone or Download:**
    - Download the files from this repository to a folder on your computer.

3.  **Create Your `.env` File:**
    - Create a copy of the `.env.example` file and rename it to `.env`.
    - Open `.env` and fill in your actual `TELEGRAM_TOKEN` and the comma-separated `CHAT_IDS`.

4.  **Set Up a Virtual Environment:**
    - Open a terminal in the project folder and run:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

5.  **Install Libraries:**
    - With the virtual environment active, install the required libraries:
    ```bash
    pip install python-telegram-bot python-dotenv
    ```
---

## ## 🚀 Running the Bot

### Local Testing
To test the bot on your own computer, simply run:
```bash
python main.py
```
*Note: This will run the script once. The daily scheduling is handled by the deployment service.*

### Deployment on PythonAnywhere (Recommended)

1.  **Upload Files:** Upload `main.py` and your completed `.env` file to your PythonAnywhere file storage.
2.  **Install Libraries:** Open a Bash console on PythonAnywhere and run `pip<version> install --user python-telegram-bot python-dotenv`. (e.g., `pip3.13`).
3.  **Schedule the Task:**
    - Go to the **Tasks** tab.
    - Schedule a new daily task for the UTC time you want.
    - Set the command to `python<version> /home/YourUsername/main.py` (e.g., `python3.13`).

---

## ## 🛠️ `find_id.py` Utility
If you need to find the Chat ID for a new group, use the included helper script.

1.  Make sure the bot is a member of the new group.
2.  Run the script locally: `python find_id.py`
3.  Send any message in the group, and the Chat ID will be printed in your terminal.
