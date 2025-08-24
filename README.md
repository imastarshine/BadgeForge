# Badge Forge Tool

This bot allows you to create badges on Roblox and receive notifications via Telegram if any errors occur. Follow the steps below to set up the project.

---

## 1. Create an X-API-Key

1. Go to this [webpage](https://create.roblox.com/dashboard/credentials?activeTab=ApiKeysTab).
2. Click **Create API Key**.
3. In **Access Permissions**, select `universe` and choose the place you want to work with.
    - Add the `universe.place:write` and `universe:write` permissions.
4. Still in **Access Permissions**, select `legacy-badges`.
    - Add all the rules provided for it.

## 2. Prepare Files

All files should be placed in the **main project directory**.

### Required files:

1. **`telegram_token.txt`** — your Telegram bot token.  
   Create this file and paste your token inside.

2. **`robloxtoken.txt`** — your Roblox X-API-Key.  
   Create this file and paste your API key inside.

3. **`badge_logs.txt`** — log file for the bot.  
   You can create an empty file.

4. **`badgeno.json`** — keeps track of badge progress.  
   Create this file with the following content:
   ```json
   {
       "current_badge": 0,
       "free_badges": 0
   }

5. **`badge.png`** — the badge image.
   Place the image named `badge.png` in the main directory.

---

## 2. Set Up Virtual Environment

### Linux / macOS:

```bash
# Go to project directory
cd /path/to/project

# Create virtual environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate

# Install dependencies
pip install requests
```

### Windows (cmd):

```cmd
# Go to project directory
cd C:\path\to\project

# Create virtual environment
python -m venv .venv

# Activate environment
.venv\Scripts\activate

# Install dependencies
pip install requests
```

---

## 3. Run the Bot

Once everything is ready and the virtual environment is activated:

```bash
python main.py
```

* The bot will start and use tokens from `telegram_token.txt` and `robloxtoken.txt`.
* Logs will be saved to `badge_logs.txt`.

---

## 4. Important Notes

* All files must stay in the **main project directory**.
* `badgeno.json` will be automatically updated by the bot during operation.
