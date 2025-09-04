import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Simple webserver
app = Flask(__name__)

@app.route('/')
def home():
    return "Claimed Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Events
@bot.event
async def on_ready():
    print(f"🖤 Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🖤")

# Run bot
keep_alive()
bot.run(os.getenv("BOT_TOKEN"))
