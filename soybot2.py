import discord
import random
import time
from discord.ext import commands
from modules.randomwiki import *
from modules.tcp import *
from modules.baccy import *
from modules.handout import giveHandout
from datetime import datetime
from dateutil import parser
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


client = commands.Bot(command_prefix='!', intents=intents)

handoutLog = {
    123456789: "2024-11-06 13:31:50",
    123456789: "2024-11-06 13:31:50",
    123456789: "2024-11-06 13:31:50",
    123456789: "2024-11-06 13:31:50",
}


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
    now = datetime.now()
    userId = ctx.author.id
    claimedDate = parser.parse(handoutLog[userId])
    if (now - claimedDate).days >= 1:
        if (giveHandout(str(ctx.author.id))):
            await ctx.send("Check your paypal")
            handoutLog[userId] = " ".join(str(now).split(".")[0:-1])
        else:
            await ctx.send("Soybot's wallet is empty.")
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
    tcpGame = returnGame(int(message.split()[1]), str(ctx.author.id))
    await ctx.send(f"Player hand: {tcpGame[0]}")
    await ctx.send(f"Dealer hand: {tcpGame[1]}")
    await ctx.send(f"{tcpGame[2]} with a {tcpGame[3]}")


@client.command(name="baccy")
async def baccy(ctx):
    game = baccyGame()
    print(game)
    await ctx.send(f"Player hand: {game[0]}\nPlayer total: {game[1]}")
    await ctx.send(f"Banker hand: {game[2]}\nBanker total: {game[3]}")
    await ctx.send("-----------------------------------------")
    time.sleep(2)
    await ctx.send(f"Player hand: {game[4]}\nPlayer total: {game[5]}")
    await ctx.send(f"Banker hand: {game[6]}\nBanker total: {game[7]}")
    await ctx.send(game[8])


@client.command(name="balance")
async def balance(ctx):
    with open("assets/balances.txt", "r") as f:
        bals = [x.strip().split(" ") for x in f.readlines()]
        for x in bals:
            if x[0] == str(ctx.author.id):
                await ctx.send(f"Your balance is: {x[1]}")


@client.command(name="leaderboard")
async def leaderboard(ctx):
    t = []
    r = []
    with open("assets/balances.txt", "r") as f:
        balances = sorted([int(x.strip().split()[1])
                          for x in f.readlines()], reverse=True)
        for bal in balances:
            f.seek(0)
            for line in f.readlines():
                if str(bal) in line.strip() and line.strip() not in t:
                    t.append(line.strip())
    for x in t:
        x = x.split()
        r.append(f"{str(client.get_user(int(x[0]))).replace("_", "")}: {x[1]}")
    await ctx.send("\n".join(r))
