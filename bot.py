import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
from pymongo import MongoClient

# ---- Bot Setup ----
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---- Web Server for Uptime ----
app = Flask(__name__)

@app.route('/')
def home():
    return "Claimed Bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ---- Database Setup ----
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["claimedbot"]
users = db["users"]

# ---- Bot Commands ----
@bot.event
async def on_ready():
    print(f"🖤 Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🖤")

@bot.command()
async def balance(ctx):
    user_id = str(ctx.author.id)
    user = users.find_one({"_id": user_id})
    if not user:
        users.insert_one({"_id": user_id, "balance": 100})
        balance = 100
    else:
        balance = user["balance"]
    await ctx.send(f"💰 {ctx.author.mention}, your balance is **{balance} coins**.")

@bot.command()
async def work(ctx):
    user_id = str(ctx.author.id)
    user = users.find_one({"_id": user_id})
    if not user:
        users.insert_one({"_id": user_id, "balance": 100})
        balance = 100
    else:
        balance = user["balance"] + 50
        users.update_one({"_id": user_id}, {"$set": {"balance": balance}})
    await ctx.send(f"🛠️ {ctx.author.mention}, you worked and earned 50 coins! Balance: **{balance} coins**.")

# ---- Run Bot ----
keep_alive()
bot.run(os.getenv("BOT_TOKEN"))
