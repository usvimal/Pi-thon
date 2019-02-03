import discord
import os
import platform
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
	print('Logged in as ' + str(client.user.name) + ' (ID:' + str(client.user.id) + ') | Connected to ' + str(len(client.guilds)) + ' servers | Connected to ' + str(len(set(client.get_all_members()))) + ' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,platform.python_version()))
	await client.change_presence(activity=discord.Game(name='epic games'))
	return


@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return

	# deletes your message and talks through the bot
	if message.content.startswith(';bot'):
		await client.delete_message(message)
		msg = message.content.split(' ')
		msg = ' '.join(msg[1:])
		print(message.author.id)
		if message.author.id == Vimal or message.author.id == Cilian or message.author.id == WY:
			msg = msg.format(message)
			await message.channel.send(msg)
			return
		else:
			msg = ('You are not authorised sorry! {0.author.mention}').format(message)
			await message.channel.send(msg)
			return
		return

token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
