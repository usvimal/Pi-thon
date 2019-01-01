import discord
import os
import asyncio

from asyncio.subprocess import PIPE
from discord.ext import commands

client = discord.Client()

Vimal = "274578439783317514"
Cilian = "424781702779633684"
WY = "260781340608167938"

@client.event
# outputs in log when bot is logged in
async def on_ready():
    print("*Hackerman voice* I'm in")
    print(client.user)
    await client.change_presence(game=discord.Game(name='epic games'))
    return
			
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
