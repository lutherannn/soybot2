import discord
import random
import time
from discord.ext import commands
from modules.randomwiki import *
from modules.tcp import *
from modules.baccy import *
from modules.wallets import Ledger
from modules.war import *

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(f"Logged on as {client.user}")


@client.event
async def on_message(message):
    await client.process_commands(message)


@client.command(name="roll")
async def roll(ctx):
    r = ""
    for _ in range(10):
        r += str(random.randrange(0, 9))
    await ctx.send(r)


@client.command(name="wheel")
async def wheel(ctx):
    await ctx.send(random.choice(["1", "2", "3", "4", "5"]))


@client.command(name="roll20")
async def roll20(ctx):
    await ctx.send(random.randrange(0, 21))


@client.command(name="handout")
async def handout(ctx):
    x = Ledger()
    if x.is_handout_valid(str(ctx.author.id)):
        x.update_balance_by_authorid(str(ctx.author.id), 1000)
        await ctx.send("Check your paypal")
        await ctx.send(f"Your new balance: {x.find_wallet_by_authorid(ctx.author.id).balance}")
    else:
        await ctx.send("You already claimed your daily cash")


@client.command(name="soyroulette")
async def soyroulette(ctx):
    await ctx.send("BANG!" if random.randrange(1, 7) == 6 else "Click.")


@client.command(name="randomwiki")
async def randomwiki(ctx):
    r = getArticle()
    await ctx.send(f"Here is the summarized article on {r[0].title()}")
    await ctx.send(r[1])
    await ctx.send(f"Link: {r[2]}")


@client.command(name="tcp")
async def tcp(ctx):
    message = ctx.message.content
    if int(message.split()[1]) < 0:
        await ctx.send("Bet must be greater than 0")
    else:
        tcpGame = returnTcpGame(int(message.split()[1]), str(ctx.author.id))
        await ctx.send(f"Player hand: {tcpGame[0]}")
        await ctx.send(f"Dealer hand: {tcpGame[1]}")
        await ctx.send(f"{tcpGame[2]} with a {tcpGame[3]}")


@client.command(name="baccy")
async def baccy(ctx):
    game = returnBaccyGame()
    await ctx.send(f"Player hand: {game[0]}\nPlayer total: {game[1]}")
    await ctx.send(f"Banker hand: {game[2]}\nBanker total: {game[3]}")
    await ctx.send("-----------------------------------------")
    time.sleep(2)
    await ctx.send(f"Player hand: {game[4]}\nPlayer total: {game[5]}")
    await ctx.send(f"Banker hand: {game[6]}\nBanker total: {game[7]}")
    await ctx.send(game[8])


@client.command(name="war")
async def war(ctx):
    message = ctx.message.content
    if int(message.split()[1]) < 0:
        await ctx.send("Bet must be greater than 0")
    else:
        game = returnWarGame(int(message.split()[1]), str(ctx.author.id))
        await ctx.send(game)


@client.command(name="balance")
async def balance(ctx):
    x = Ledger().find_wallet_by_authorid(str(ctx.author.id))
    if x:
        await ctx.send(f"Your balance is: {x.balance}")
    else:
        await ctx.send("Couldn't find your account")


@client.command(name="leaderboard")
async def leaderboard(ctx):
    ledger = Ledger()
    ledger._load_ledger()

    sorted_wallets = sorted(
        ledger.wallets, key=lambda wallet: wallet.balance, reverse=True
    )

    leaderboard_entries = [
        f"{str(client.get_user(int(wallet.authorid))
               ).replace('_', '')}: {wallet.balance}"
        for wallet in sorted_wallets
    ]

    await ctx.send("\n".join(leaderboard_entries))
