# 🖤 ClaimedBot

ClaimedBot is a **Discord bot** built for fun, community, and economy features.  
It is designed to run **24/7 for free** using **Render, MongoDB Atlas, and UptimeRobot**.

---

## ✨ Features
- ⚡ `!ping` → Check if the bot is alive.  
- 💰 `!balance` → See your coin balance.  
- 🛠️ `!work` → Work to earn coins.  
- 🔒 Secure database storage with MongoDB Atlas.  
- 🌍 Free 24/7 uptime using Flask + UptimeRobot.  

---

## 🛠️ Setup Guide

### 1. Clone the repository
```git clone https://github.com/YOUR_USERNAME/claimedbot.git```
```cd claimedbot```

### 2. Install dependencies
```pip install -r requirements.txt```

### 3. Environment Variables

Create a .env file (for local testing) or add these in Render’s Environment settings:

```BOT_TOKEN=your_discord_bot_token_here```
```MONGO_URI=your_mongodb_connection_uri_here```

### 4. Run the bot

```python bot.py```

## 🚀 Deployment

This bot is deployed for free using:

### Render
 → Python hosting

### MongoDB Atlas
 → Free database

### UptimeRobot
 → Keeps bot alive 24/7

## 📦 requirements.txt

Make sure your requirements.txt file contains the following:

```discord.py```
```flask```
```pymongo```
```dnspython```

## 📜 License

This project is open-source under the MIT License.

## 🤝 Contributing

Pull requests are welcome! Feel free to suggest features or improvements.

## 👤 Author

Made with 🖤 by Nanami

---
