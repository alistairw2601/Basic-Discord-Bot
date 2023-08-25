import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import random
import asyncio

coin=["heads","tails"]
f=open("coinscore.txt",mode="r")
file=f.read()
list=file.splitlines()
splitlist=[]
for x in list:
    g=x.split(",")
    splitlist.append(g)
print(splitlist)
f.close()

client = commands.Bot(command_prefix="=", intents=discord.Intents.all())

bot_status = cycle(["Hello","use the prefix =","=help for commands"])

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

f=open("BotToken.txt",mode='r')
token=f.read()
f.close()

@tasks.loop(seconds=3)
async def status_change():
    await client.change_presence(activity=discord.Game(next(bot_status)))


@client.event
async def on_ready():
    print("Bot is connected")
    status_change.start()

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if "=help" in message.content:
        await message.channel.send("=dice   roll a dice.\n\n=coinflip   flip a coin.\n\n=coinguess   put either heads, tails or stats after this command to bet on the outcome or to view your stats at this game.")

    if "=dice" in message.content:
        await  message.channel.send(f"You rolled {random.randint(1,6)}!")

    if "=coinflip" in message.content:
        result=random.choice(coin)
        await message.channel.send(f"The coin landed on {result}")
    listnum="no"

    if message.content.startswith("=coinguess"):
        msgauth=message.author.name
        for x in range(len(splitlist)):
            if splitlist[x][0]==msgauth:
                listnum=x
                break
        if listnum=="no":
            splitlist.append([message.author.name,"0","0","0","0"])
            listnum=len(splitlist)-1

        guess=message.content[11:]
        if guess not in coin:
            if guess=="stats":
                stats=f"Stats for {splitlist[listnum][0]}:\nTosses: {splitlist[listnum][1]}\nWins: {splitlist[listnum][2]}\nCurrent Streak: {splitlist[listnum][3]}\nBest Streak: {splitlist[listnum][4]}"
                await message.channel.send(stats)
            else:
                await message.channel.send(f"{guess} is not a valid choice.")
        else:
            result = random.choice(coin)
            if guess == result:
                plays=int(splitlist[listnum][1])+1
                splitlist[listnum][1]=str(plays)
                wins = int(splitlist[listnum][2]) + 1
                splitlist[listnum][2] = str(wins)
                streak = int(splitlist[listnum][3]) + 1
                splitlist[listnum][3] = str(streak)
                if streak>int(splitlist[listnum][4]):
                    splitlist[listnum][4]=str(streak)

                    rewrite=[]
                    for x in splitlist:
                        y=",".join(x)
                        rewrite.append(y)
                    f=open("coinscore.txt",mode="w")
                    for x in rewrite:
                        f.write(x+"\n")
                    f.close()

                await message.channel.send(f"It was {result}. You win!")
            else:
                plays = int(splitlist[listnum][1]) + 1
                splitlist[listnum][1] = str(plays)
                streak = 0
                splitlist[listnum][3] = str(streak)
                rewrite = []
                for x in splitlist:
                    y = ",".join(x)
                    rewrite.append(y)
                f = open("coinscore.txt", mode="w")
                for x in rewrite:
                    f.write(x + "\n")
                f.close()
                await message.channel.send(f"It was {result}. You lose.")

client.run(token)
run=True
while run==True:
    x=input("Please enter STOP if you would like to stop the bot")
    if x == 'STOP':
        run=False
