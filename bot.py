import discord
from discord.ext import commands
import random
import os

# TOKEN artık koda yazılmaz
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} aktif!")

@bot.command()
async def ping(ctx):
    await ctx.send("pong 🏓")

@bot.command()
async def sa(ctx):
    await ctx.send("as kanka")

@bot.command()
async def coin(ctx):
    await ctx.send(random.choice(["Yazı", "Tura"]))

bot.run(TOKEN)
