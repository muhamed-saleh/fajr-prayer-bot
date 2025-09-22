# Fajr Prayer Poll Bot (بوت صلاة الفجر)

<img width="858" height="140" alt="image" src="https://github.com/user-attachments/assets/e544ebab-930b-417f-b619-9f0d3877f0aa" />

A sophisticated, automated Telegram bot that sends a daily poll to multiple groups one hour before Fajr prayer to encourage users to wake up for Tahajjud (قيام الليل) and Fajr.

The bot is timezone-aware, fetches prayer times dynamically from the Aladhan API, and is designed to be deployed on a server like PythonAnywhere for 24/7 operation.

---

## ## ✨ Features

- **Automated Daily Polls:** Schedules and sends polls automatically every day.
- **Dynamic Prayer Times:** Fetches daily Fajr prayer times for a specific city.
- **Timezone Aware:** Correctly handles the difference between the server's UTC time and the local timezone of the target city.
- **Pre-Fajr Reminder:** Sends the poll exactly one hour before Fajr, serving as a perfect reminder for Tahajjud prayer.
- **Multi-Group Support:** Manages and sends polls to an unlimited number of groups via a clean JSON configuration.
- **Dynamic Question:** The poll question is automatically updated with the current date in Arabic.
- **Management Tools:** Includes helper scripts to instantly send polls and manage the group list from the command line without manual JSON editing.

---

## ## 📂 Project Structure

```
.
├── .env.example        # Template for environment variables
├── .gitignore          # Specifies files for Git to ignore
├── config.json         # Stores the list of groups (names and IDs)
├── find_id.py          # Utility script to find a group's Chat ID
├── instant_poll.py     # Script to send a poll immediately on demand
├── main.py             # The main script for the daily scheduled poll
├── manager.py          # Command-line tool to manage the group list
└── requirements.txt    # Lists all required Python libraries
```

---

## ## ⚙️ Setup Instructions

#### 1. Get a Bot Token
- Talk to the [@BotFather](https://t.me/BotFather) on Telegram to create a new bot and get its API token.
- Go to your bot's settings in BotFather and disable "Group Privacy" so it can read messages in groups.

#### 2. Clone the Repository
- On your local machine, clone the repository:
  ```bash
  git clone [https://github.com/muhamed-saleh/fajr-prayer-bot.git](https://github.com/muhamed-saleh/fajr-prayer-bot.git)
  cd fajr-prayer-bot
  ```

#### 3. Create Your `.env` File
- Create a copy of `.env.example` and rename it to `.env`.
- Open `.env` and add your secret Telegram Bot Token:
  ```ini
  TELEGRAM_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u1234saken"
  ```

#### 4. Set Up a Virtual Environment
- Create and activate a Python virtual environment:
  ```bash
  python -m venv venv
  # On Windows
  .\venv\Scripts\activate
  # On macOS/Linux
  source venv/bin/activate
  ```

#### 5. Install Dependencies
- Install all the required libraries from the `requirements.txt` file:
  ```bash
  pip install -r requirements.txt
  ```

---

## ## 🚀 Usage

### Managing Your Group List
Use the `manager.py` script to easily manage your `config.json` file.

- **To list all groups:**
  ```bash
  python manager.py list
  ```
- **To add a new group:** (Use quotes for names with spaces)
  ```bash
  python manager.py add "My Family Group" -100123456789
  ```
- **To remove a group by name:**
  ```bash
  python manager.py remove "My Family Group"
  ```

### Sending an Instant Poll (For Testing)
To send a poll immediately to all configured groups, run:
```bash
python instant_poll.py
```

---

## ## ☁️ Deployment on PythonAnywhere

This bot is designed to be deployed as a scheduled task.

1.  **Upload/Clone Project:**
    - On the PythonAnywhere **Files** tab, open a **Bash console**.
    - Clone your repository: `git clone https://github.com/muhamed-saleh/fajr-prayer-bot.git`

2.  **Create Your Files:**
    - In the new `fajr-prayer-bot` folder, create your `.env` and `config.json` files with your token and group info.

3.  **Install Libraries:**
    - In the console, install the dependencies using your desired Python version:
      ```bash
      pip3.13 install --user -r fajr-prayer-bot/requirements.txt
      ```

4.  **Schedule the Daily Task:**
    - Go to the **Tasks** tab.
    - Create a new **Daily** task.
    - Set the time to an early UTC hour (e.g., `23:00 UTC`).
    - Set the command to the full path of your main script, including the project folder:
      ```bash
      python3.13 /home/YourUsername/fajr-prayer-bot/main.py
      ```
    - Save the task, and your bot will run automatically every day.

---

## ## 📄 License
This project is licensed under the MIT License. See the `LICENSE` file for details.
