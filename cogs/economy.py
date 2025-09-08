import random
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from db import users, daily_claims, get_user
from datetime import datetime

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx):
        user = get_user(str(ctx.author.id))
        await ctx.send(f"💰 {ctx.author.mention}, your balance is **{user['balance']} coins**.")

    @commands.command()
    @cooldown(1, 3600, BucketType.user)
    async def work(self, ctx):
        user_id = str(ctx.author.id)
        user = get_user(user_id)
        earnings = random.randint(40, 100)
        new_balance = user["balance"] + earnings
        users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
        await ctx.send(f"🛠️ {ctx.author.mention}, you worked and earned {earnings} coins! Balance: **{new_balance} coins**.")

    @commands.command()
    @cooldown(1, 86400, BucketType.user)
    async def daily(self, ctx):
        user_id = str(ctx.author.id)
        today = datetime.utcnow().date()
        claim = daily_claims.find_one({"_id": user_id})

        if claim and claim["last_claim"] == str(today):
            await ctx.send("⏳ You already claimed your daily coins today!")
            return

        reward = 200
        user = get_user(user_id)
        new_balance = user["balance"] + reward
        users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
        daily_claims.update_one({"_id": user_id}, {"$set": {"last_claim": str(today)}}, upsert=True)

        await ctx.send(f"🌞 {ctx.author.mention}, you claimed your daily **{reward} coins**! Balance: **{new_balance} coins**.")

    @commands.command()
    async def give(self, ctx, member, amount: int):
        if amount <= 0:
            await ctx.send("❌ Amount must be positive.")
            return
        sender_id = str(ctx.author.id)
        receiver_id = str(member.id)

        if sender_id == receiver_id:
            await ctx.send("❌ You cannot give coins to yourself!")
            return

        sender = get_user(sender_id)
        if sender["balance"] < amount:
            await ctx.send("❌ You don't have enough coins!")
            return

        users.update_one({"_id": sender_id}, {"$inc": {"balance": -amount}})
        users.update_one({"_id": receiver_id}, {"$inc": {"balance": amount}})

        await ctx.send(f"💸 {ctx.author.mention} gave {amount} coins to {member.mention}!")

async def setup(bot):
    await bot.add_cog(Economy(bot))
