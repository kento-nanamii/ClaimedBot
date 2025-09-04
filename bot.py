import os
import discord
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType
from flask import Flask
from threading import Thread
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

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
    return "ClaimedBot is alive 🖤"

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
daily_claims = db["daily_claims"]  # For daily rewards

# ---- Helper Functions ----
def get_user(user_id):
    user = users.find_one({"_id": user_id})
    if not user:
        users.insert_one({"_id": user_id, "balance": 100})
        return {"_id": user_id, "balance": 100}
    return user

# ---- Bot Events ----
@bot.event
async def on_ready():
    print(f"🖤 Logged in as {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Slow down! Try again in {round(error.retry_after)} seconds.")
    else:
        await ctx.send("❌ Something went wrong.")
        raise error

# ---- Bot Commands ----
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🖤")

@bot.command()
async def balance(ctx):
    user = get_user(str(ctx.author.id))
    await ctx.send(f"💰 {ctx.author.mention}, your balance is **{user['balance']} coins**.")

@bot.command()
@cooldown(1, 3600, BucketType.user)  # 1 hour cooldown
async def work(ctx):
    user_id = str(ctx.author.id)
    user = get_user(user_id)
    earnings = random.randint(40, 100)
    new_balance = user["balance"] + earnings
    users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
    await ctx.send(f"🛠️ {ctx.author.mention}, you worked and earned {earnings} coins! Balance: **{new_balance} coins**.")

@bot.command()
@cooldown(1, 86400, BucketType.user)  # 24 hour cooldown
async def daily(ctx):
    user_id = str(ctx.author.id)
    today = datetime.utcnow().date()
    claim = daily_claims.find_one({"_id": user_id})
    if claim and claim["last_claim"] == str(today):
        await ctx.send("⏳ You have already claimed your daily coins today!")
        return
    reward = 200
    user = get_user(user_id)
    new_balance = user["balance"] + reward
    users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
    daily_claims.update_one({"_id": user_id}, {"$set": {"last_claim": str(today)}}, upsert=True)
    await ctx.send(f"🌞 {ctx.author.mention}, you claimed your daily **{reward} coins**! Balance: **{new_balance} coins**.")

@bot.command()
async def give(ctx, member: discord.Member, amount: int):
    if amount <= 0:
        await ctx.send("❌ Amount must be positive.")
        return
    sender_id = str(ctx.author.id)
    receiver_id = str(member.id)
    sender = get_user(sender_id)
    receiver = get_user(receiver_id)
    if sender["balance"] < amount:
        await ctx.send("❌ You don't have enough coins!")
        return
    users.update_one({"_id": sender_id}, {"$inc": {"balance": -amount}})
    users.update_one({"_id": receiver_id}, {"$inc": {"balance": amount}})
    await ctx.send(f"💸 {ctx.author.mention} gave {amount} coins to {member.mention}!")

# ---- Admin Command Example ----
@bot.command()
@commands.has_permissions(administrator=True)
async def reset_balance(ctx, member: discord.Member):
    users.update_one({"_id": str(member.id)}, {"$set": {"balance": 100}}, upsert=True)
    await ctx.send(f"🔄 {member.mention}'s balance has been reset to 100 coins.")

# ---- Run Bot ----
keep_alive()
bot.run(os.getenv("BOT_TOKEN"))
