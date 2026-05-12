import discord
from discord.ext import commands
import random
import os

TOKEN = os.getenv("TOKEN")

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
# COIN FLIP (BAHİSLİ)
# ─────────────────────────────
@bot.command()
async def coin(ctx, amount: int, choice: str):
    user = ctx.author.id

    if user not in balances:
        balances[user] = 1000

    if amount <= 0:
        await ctx.send("Geçerli bir bahis gir 😄")
        return

    if amount > balances[user]:
        await ctx.send("Yetersiz coin 😄")
        return

    choice = choice.lower()
    if choice not in ["yazı", "tura"]:
        await ctx.send("Sadece 'yazı' veya 'tura' yaz 😄")
        return

    result = random.choice(["yazı", "tura"])

    if choice == result:
        balances[user] += amount
        await ctx.send(f"🎉 Kazandın +{amount} coin | Sonuç: {result}")
    else:
        balances[user] -= amount
        await ctx.send(f"😭 Kaybettin -{amount} coin | Sonuç: {result}")

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
        f"🃏 BLACKJACK BAŞLADI\n"
        f"Sen: {sum(player)}\n"
        f"Dealer: {dealer[0]} + ?\n"
        f"!hit veya !stand yaz"
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
        await ctx.send(f"💥 BUST! Kaybettin")
    else:
        await ctx.send(f"Sen: {total} | !hit / !stand")

# ─────────────────────────────
# STAND (DEALER AI)
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
        f"🃏 SONUÇ\n"
        f"Sen: {player_score}\n"
        f"Dealer: {dealer_score}\n\n"
        f"{result}"
    )

# ─────────────────────────────
# SA / PING
# ─────────────────────────────
@bot.command()
async def sa(ctx):
    await ctx.send("as kanka")

@bot.command()
async def ping(ctx):
    await ctx.send("pong 🏓")

# ─────────────────────────────
# BOT RUN
# ─────────────────────────────
bot.run(TOKEN)
