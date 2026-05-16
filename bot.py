import discord
from discord.ext import commands
import random
import os
import time

TOKEN = os.getenv("TOKEN")

OWNER_ID = 815578764704219136

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

balances = {}
active_games = {}
daily_cooldown = {}
work_cooldown = {}

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

    await ctx.send(f" Bakiyen: {balances[user]} coin")

# ─────────────────────────────
# RECOVERY
# ─────────────────────────────
@bot.command()
async def recovery(ctx):

    user = ctx.author.id

    if user not in balances:
        balances[user] = 0

    if balances[user] > 0:
        await ctx.send(" Recovery sadece 0 coin iken kullanılabilir")
        return

    balances[user] = 300

    await ctx.send(" +300 coin verildi")

# ─────────────────────────────
# ADMIN MONEY
# ─────────────────────────────
@bot.command()
async def addmoney(ctx, member: discord.Member, amount: int):

    if ctx.author.id != OWNER_ID:
        await ctx.send(" Yetkin yok")
        return

    user = member.id

    if user not in balances:
        balances[user] = 1000

    balances[user] += amount

    await ctx.send(f" {member.mention} kullanıcısına +{amount} coin verildi")

# ─────────────────────────────
# COIN FLIP
# ─────────────────────────────
@bot.command()
async def coin(ctx, amount: int, choice: str):

    user = ctx.author.id

    if user not in balances:
        balances[user] = 1000

    if amount <= 0 or amount > balances[user]:
        await ctx.send(" Yetersiz coin")
        return

    choice = choice.lower()

    if choice not in ["yazı", "tura"]:
        await ctx.send("yazı / tura yaz")
        return

    result = random.choice(["yazı", "tura"])

    if result == choice:
        balances[user] += amount
        await ctx.send(f"✅ +{amount} coin kazandın | Sonuç: {result}")

    else:
        balances[user] -= amount
        await ctx.send(f"❌ -{amount} coin kaybettin | Sonuç: {result}")

# ─────────────────────────────
# SLOT MACHINE
# ─────────────────────────────
@bot.command()
async def slot(ctx, bet: int):

    user = ctx.author.id

    if user not in balances:
        balances[user] = 1000

    if bet <= 0 or bet > balances[user]:
        await ctx.send(" Yetersiz coin")
        return

    symbols = ["🍒", "🍋", "🍇", "💎", "7️⃣"]

    a = random.choice(symbols)
    b = random.choice(symbols)
    c = random.choice(symbols)

    result = f"{a} | {b} | {c}"

    # JACKPOT
    if a == b == c:

        win = bet * 5
        balances[user] += win

        await ctx.send(f" {result}\n💎 JACKPOT! +{win}")

    # İKİ AYNI
    elif a == b or b == c or a == c:

        win = bet * 2
        balances[user] += win

        await ctx.send(f" {result}\n✅ Kazandın! +{win}")

    # KAYBET
    else:

        balances[user] -= bet

        await ctx.send(f" {result}\n❌ Kaybettin! -{bet}")

# ─────────────────────────────
# BLACKJACK
# ─────────────────────────────
@bot.command()
async def blackjack(ctx, bet: int):

    user = ctx.author.id

    if user not in balances:
        balances[user] = 1000

    if bet <= 0 or bet > balances[user]:
        await ctx.send(" Yetersiz coin")
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
        await ctx.send(" Aktif oyun yok")
        return

    game = active_games[user]

    def draw():
        return random.randint(1, 10)

    game["player"].append(draw())

    total = sum(game["player"])

    if total > 21:

        balances[user] -= game["bet"]

        del active_games[user]

        await ctx.send(f" BUST! Toplam: {total}")

    else:

        await ctx.send(f" Yeni kart çekildi\nToplam: {total}")

# ─────────────────────────────
# STAND
# ─────────────────────────────
@bot.command()
async def stand(ctx):

    user = ctx.author.id

    if user not in active_games:
        await ctx.send("❌ Aktif oyun yok")
        return

    game = active_games[user]

    def draw():
        return random.randint(2, 11)

    dealer = game["dealer"]
    dealer_score = sum(dealer)

    while dealer_score < 17:
        dealer.append(draw())
        dealer_score = sum(dealer)

    player_score = sum(game["player"])
    bet = game["bet"]

    if dealer_score > 21 or player_score > dealer_score:

        balances[user] += bet
        result = f" Kazandın! +{bet}"

    elif player_score < dealer_score:

        balances[user] -= bet
        result = f" Kaybettin! -{bet}"

    else:

        result = " Berabere"

    del active_games[user]

    await ctx.send(
        f"🃏 SONUÇ\n"
        f"Sen: {player_score}\n"
        f"Dealer: {dealer_score}\n"
        f"{result}"
    )

# ─────────────────────────────
# DICE
# ─────────────────────────────
@bot.command()
async def dice(ctx, bet: int):

    user = ctx.author.id

    if user not in balances:
        balances[user] = 1000

    if bet <= 0 or bet > balances[user]:
        await ctx.send(" Yetersiz coin")
        return

    player = random.randint(1, 6)
    dealer = random.randint(1, 6)

    if player > dealer:

        balances[user] += bet

        result = (
            f" Sen: {player}\n"
            f" Dealer: {dealer}\n"
            f" Kazandın +{bet}"
        )

    elif player < dealer:

        balances[user] -= bet

        result = (
            f" Sen: {player}\n"
            f" Dealer: {dealer}\n"
            f" Kaybettin -{bet}"
        )

    else:

        result = (
            f" Sen: {player}\n"
            f" Dealer: {dealer}\n"
            f" Berabere"
        )

    await ctx.send(result)

# ─────────────────────────────
# DAILY
# ─────────────────────────────
@bot.command()
async def daily(ctx):

    user = ctx.author.id
    now = time.time()

    if user not in balances:
        balances[user] = 1000

    if user in daily_cooldown:

        elapsed = now - daily_cooldown[user]

        if elapsed < 86400:

            remaining = int(86400 - elapsed)

            hours = remaining // 3600
            minutes = (remaining % 3600) // 60

            await ctx.send(
                f" Daily zaten alınmış\n"
                f"Kalan süre: {hours}s {minutes}dk"
            )

            return

    reward = random.randint(200, 500)

    balances[user] += reward
    daily_cooldown[user] = now

    await ctx.send(f" Daily aldın! +{reward} coin")

# ─────────────────────────────
# TOP
# ─────────────────────────────
@bot.command()
async def top(ctx):

    if not balances:
        await ctx.send(" Hiç kullanıcı yok")
        return

    sorted_balances = sorted(
        balances.items(),
        key=lambda x: x[1],
        reverse=True
    )

    text = " Sıralama:\n\n"

    for i, (user_id, balance) in enumerate(sorted_balances[:10], start=1):

        user = await bot.fetch_user(user_id)

        text += f"{i}. {user.name} - {balance} coin\n"

    await ctx.send(text)

# ─────────────────────────────
# BASIC
# ─────────────────────────────
@bot.command()
async def sa(ctx):
    await ctx.send("as kanka")

@bot.command()
async def ping(ctx):
    await ctx.send(" pong")

#--------------------------
#!work
@bot.command()
async def work(ctx):

    user = ctx.author.id
    now = time.time()

    if user not in balances:
        balances[user] = 1000

        #cooldown
        if user in work_cooldown:

            if now - work_cooldown[user] < 600:

                remaining = int(600 - (now - work_cooldown[user]))
                minutes = remaining // 60
                seconds = remaining % 60

                await ctx.send(f"Work cooldown: {mintues}dk {seconds}sn kaldı")
                return
            
            earnings = random.randtint(80,200)

            balances[user] += earnings
            work_cooldown[user] = now

            await ctx.send(f"Çalıştın ve +{earnings} coin kazandın")

# ─────────────────────────────
# RUN
# ─────────────────────────────
bot.run(TOKEN) 