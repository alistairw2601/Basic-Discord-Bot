import shutil
import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
import random

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

    if "=dice" in message.content:
        await  message.channel.send(f"You rolled {random.randint(1,6)}!")
    if "=coinflip" in message.content:
        coin=["heads","tails"]
        result=random.choice(coin)
        await message.channel.send(f"The coin landed on {result}")

client.run(token)
