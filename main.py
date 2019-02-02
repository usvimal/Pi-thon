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
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')

	await client.change_presence(game=discord.Game(name='epic games'))
	return
			
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
