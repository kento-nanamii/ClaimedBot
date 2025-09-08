import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load all cogs automatically
initial_cogs = ["economy", "banking", "leaderboard", "admin"]
for cog in initial_cogs:
    bot.load_extension(f"cogs.{cog}")

@bot.event
async def on_ready():
    print(f"🖤 Logged in as {bot.user}")

keep_alive()
bot.run(os.getenv("BOT_TOKEN"))
