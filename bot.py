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
# RECOVERY (SADECE 0 İKEN)
# ─────────────────────────────
@bot.command()
async def recovery(ctx):
    user = ctx.author.id

    if user not in balances:
        balances[user] = 0

    if balances[user] > 0:
        await ctx.send("🟡 Recovery sadece 0 coin iken kullanılır")
        return

    balances[user] = 300
    await ctx.send("🆘 Recovery aktif: +300 coin verildi")

# ─────────────────────────────
# ADMIN MONEY (OWNER ONLY)
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

    await ctx.send(f"👑 {member.name} → +{amount} coin")

# ─────────────────────────────
# COIN FLIP (BAHİSLİ)
# ─────────────────────────────
@bot.command()
async def coin(ctx, amount: int, choice: str):
    user = ctx.author.id

    if user not in balances:
        balances[user] = 1000

    if amount <= 0:
        await ctx.send("Geçerli bahis gir 😄")
        return

    if amount > balances[user]:
        await ctx.send("Yetersiz coin 😄")
        return

    choice = choice.lower()
    if choice not in ["yazı", "tura"]:
        await ctx.send("Sadece yazı / tura 😄")
        return

    result = random.choice(["yazı", "tura"])

    if choice == result:
        balances[user] += amount
        await ctx.send(f"🎉 Kazandın +{amount} | {result}")
    else:
        balances[user] -= amount
        await ctx.send(f"😭 Kaybettin -{amount} | {result}")

# ─────────────────────────────
# BLACKJACK START
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
        await ctx.send("💥 Bust! Kaybettin")
    else:
        await ctx.send(f"Sen: {total}")

# ─────────────────────────────
# STAND
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

    while sum(dealer) < 17:
        dealer.append(draw())

    player_score = sum(game["player"])
    dealer_score = sum(dealer)
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
        f"Sen: {player_score}\nDealer: {dealer_score}\n{result}"
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
