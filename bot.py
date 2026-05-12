import discord
from discord.ext import commands
import random
import os

TOKEN = os.getenv("TOKEN")

OWNER_ID = 815578764704219136

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

balances = {}
active_games = {}

# ─────────────────────────────
# BOT READY
# ─────────────────────────────
@bot.event
async def on_ready():
    print(f"{bot.user} aktif!")

# ─────────────────────────────
# BALANCE
# ─────────────────────────────
@bot.command()
async def balance(ctx):
    user = ctx.author.id
    if user not in balances:
        balances[user] = 1000
    await ctx.send(f"💰 Bakiyen: {balances[user]} coin")

# ─────────────────────────────
# RECOVERY
# ─────────────────────────────
@bot.command()
async def recovery(ctx):
    user = ctx.author.id

    if user not in balances:
        balances[user] = 0

    if balances[user] > 0:
        await ctx.send("🟡 Recovery sadece 0 coin iken")
        return

    balances[user] = 300
    await ctx.send("🆘 +300 coin verildi")

# ─────────────────────────────
# ADMIN MONEY
# ─────────────────────────────
@bot.command()
async def addmoney(ctx, member: discord.Member, amount: int):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Yetkin yok")
        return

    user = member.id

    if user not in balances:
        balances[user] = 1000

    balances[user] += amount

    await ctx.send(f"👑 +{amount} coin verildi")

# ─────────────────────────────
# COIN FLIP
# ─────────────────────────────
@bot.command()
async def coin(ctx, amount: int, choice: str):
    user = ctx.author.id

    if user not in balances:
        balances[user] = 1000

    if amount <= 0 or amount > balances[user]:
        await ctx.send("Yetersiz coin 😄")
        return

    choice = choice.lower()
    if choice not in ["yazı", "tura"]:
        await ctx.send("yazı / tura yaz")
        return

    result = random.choice(["yazı", "tura"])

    if result == choice:
        balances[user] += amount
        await ctx.send(f"🎉 +{amount} | {result}")
    else:
        balances[user] -= amount
        await ctx.send(f"😭 -{amount} | {result}")

# ─────────────────────────────
# BLACKJACK
# ─────────────────────────────
@bot.command()
async def blackjack(ctx, bet: int):
    user = ctx.author.id

    if user not in balances:
        balances[user] = 1000

    if bet > balances[user]:
        await ctx.send("Yetersiz coin 😄")
        return

    def draw():
        return random.randint(2, 11)

    player = [draw(), draw()]
    dealer = [draw(), draw()]

    active_games[user] = {
        "bet": bet,
        "player": player,
        "dealer": dealer
    }

    await ctx.send(
        f"🃏 BLACKJACK\n"
        f"Sen: {sum(player)}\n"
        f"Dealer: {dealer[0]} + ?\n"
        f"!hit / !stand"
    )

# ─────────────────────────────
# HIT
# ─────────────────────────────
@bot.command()
async def hit(ctx):
    user = ctx.author.id

    if user not in active_games:
        await ctx.send("Oyun yok 😄")
        return

    game = active_games[user]

    def draw():
        return random.randint(2, 11)

    game["player"].append(draw())
    total = sum(game["player"])

    if total > 21:
        balances[user] -= game["bet"]
        del active_games[user]
        await ctx.send("💥 BUST!")
    else:
        await ctx.send(f"Sen: {total}")

# ─────────────────────────────
# STAND (FIXLENMİŞ DEALER)
# ─────────────────────────────
@bot.command()
async def stand(ctx):
    user = ctx.author.id

    if user not in active_games:
        await ctx.send("Oyun yok 😄")
        return

    game = active_games[user]

    def draw():
        return random.randint(2, 11)

    dealer = game["dealer"]
    dealer_score = sum(dealer)

    # ✔ FIX: 17'ye kadar çek, 21 üstü bust
    while dealer_score < 17:
        dealer.append(draw())
        dealer_score = sum(dealer)

        if dealer_score > 21:
            break

    player_score = sum(game["player"])
    bet = game["bet"]

    if dealer_score > 21 or player_score > dealer_score:
        balances[user] += bet
        result = "🎉 KAZANDIN"
    elif player_score < dealer_score:
        balances[user] -= bet
        result = "😭 KAYBETTİN"
    else:
        result = "🤝 BERABERE"

    del active_games[user]

    await ctx.send(
        f"🃏 SONUÇ\n"
        f"Sen: {player_score}\n"
        f"Dealer: {dealer_score}\n"
        f"{result}"
    )

# ─────────────────────────────
# BASIC
# ─────────────────────────────
@bot.command()
async def sa(ctx):
    await ctx.send("as kanka")

@bot.command()
async def ping(ctx):
    await ctx.send("pong 🏓")

# ─────────────────────────────
# RUN
# ─────────────────────────────
bot.run(TOKEN)
