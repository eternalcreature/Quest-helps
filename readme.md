# 🕵️ Mob Wars: Calendar Help Automation Scripts

This is a collection of Python scripts to help you quickly assist your friends with calendar events at the start of each Monthly Quest in **Mob Wars: La Cosa Nostra**.

It automates:
- Logging into KanoPlay
- Collecting friend codes of people active this month
- Clicking calendar help links for each friend

## ⚡ Quick Start

1. **Install Python** (ask ChatGPT if unsure).

2. **Open terminal** and run:

   ```bash
   python -m pip install -r requirements.txt
   playwright install
   ```

3. **Create `.env` file** with your KanoPlay login:

   ```
   KANO_EMAIL=your_email_here
   KANO_PASSWORD=your_password_here
   ```

4. Run each script in order:

   ```bash
   python step_1_login.py
   python step_2_get_mob_codes.py
   python step_3_calendar_helps.py
   ```

5. Let the last script run; it will automate clicking calendar helps for your friends.

---

For full instructions and troubleshooting, see below.


## 🧰 What You’ll Need

Before running the scripts, make sure you have:

1. **Python installed**  
   If you're not sure how, ask ChatGPT or search “how to install Python on [Windows/Mac/Linux]”.

2. **(Optional) Visual Studio Code (VS Code)**  
   A friendly editor for writing and running code. You can get it at [code.visualstudio.com](https://code.visualstudio.com).

3. **(Optional but recommended) A Python virtual environment**  
   This keeps your Python packages organized. You can ask ChatGPT: “how do I create a Python virtual environment?”

## 🚀 Getting Started

Once Python is installed, follow these steps:

### 1. Open a terminal (Command Prompt, Terminal, or VS Code terminal)

### 2. Install the required packages

```bash
python -m pip install -r requirements.txt
```

### 3. Install Playwright browser dependencies

After installing the Python packages, run this command:

```bash
playwright install
```

> This downloads the browser engines Playwright uses to automate the browser (Chromium, Firefox, WebKit). Without this, the scripts won’t be able to open or control a browser.

### 4. Create a `.env` file in the main folder

This file stores your login credentials. Create a new file named `.env` and add the following (replace the text in brackets):

```
KANO_EMAIL=[your KanoPlay email]
KANO_PASSWORD=[your KanoPlay password]
```

> 💡 Don’t include the square brackets.  
> 📁 Make sure the `.env` file is in the same folder as the `.py` files.

---

## 🧪 Step-by-Step Guide

### ✅ Step 1: Log into KanoPlay

Run this file:

```bash
python step_1_login.py
```

What it does:
- Opens a browser
- Logs into your account using the info from `.env`
- Stores your login session so future scripts can skip the login step

Run it again just to check that you're logged in (you should see the main Mob Wars homepage).

---

### 👥 Step 2: Get Mob Codes of Active Friends

```bash
python step_2_get_mob_codes.py
```

What it does:
- Opens the Mob page
- Grabs the friend codes of people who have logged in **this month**
- Stops scanning once it finds someone inactive
- Saves the codes to a file: `mob_codes.txt`

> ⏳ Don’t touch anything while this script runs.

---

### 📅 Step 3: Click Calendar Help Links

```bash
python step_3_calendar_helps.py
```

What it does:
- Opens each calendar help link for your active friends
- Waits a second between clicks (or slightly longer)
- This is automatic — just leave it running in the background

> 🕒 Depending on how many friends you have, it might take a few minutes.

---

## 🧹 Files Explained

- `.env` – your login credentials (excluded from sharing via `.gitignore`)
- `auth_data/` – saved browser session
- `mob_codes.txt` – list of your friends' user IDs
- `step_1_login.py` – logs in and stores session
- `step_2_get_mob_codes.py` – collects active friend codes
- `step_3_calendar_helps.py` – visits calendar help links
- `requirements.txt` – lists all the Python libraries you need

---

## ❓ Need Help?

If you run into problems or are unfamiliar with Python, just copy and paste your error message into ChatGPT or search online — there’s a solution for everything!

Happy helping! 🕵️‍♀️💼
