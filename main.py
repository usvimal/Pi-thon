import discord
import os
import platform
import asyncio

from asyncio.subprocess import PIPE
from discord.ext import commands

client = discord.Client()

Vimal = 274578439783317514
Cilian = 424781702779633684
WY = 260781340608167938


@client.event
# outputs in log when bot is logged in
async def on_ready():
	print("*Hackerman voice* I'm in")
	print('Logged in as ' + str(client.user.name) + ' (ID:' + str(client.user.id) + ') | Connected to ' + str(
		len(client.guilds)) + ' servers | Connected to ' + str(len(set(client.get_all_members()))) + ' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,
																			   platform.python_version()))
	await client.change_presence(activity=discord.Game(name='epic games'))
	return


@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return

	# deletes your message and talks through the bot
	if message.content.startswith(';bot'):
		await message.delete()
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

	# function list
	if message.content.lower().startswith(';help'):
		embed = discord.Embed(title="⭐ Helptext⭐ ", description="this is what I can do ;D", color=0xee0000)
		embed.add_field(name=";bot", value="talk through me", inline=True)
		embed.add_field(name=";details", value="view my code", inline=True)
		await message.channel.send(embed=embed)
		return
	# credits to haoshaun
	# vote feature, will add reactions (thumbsup and thumbsdown)
	if message.content.startswith(';vote'):
		await message.add_reaction("\U0001F44D")
		await message.add_reaction("\U0001F44E")
		await asyncio.sleep(10)
		print(message.Reaction.count("\U0001F44D"))
		print(message.Reaction.count("\U0001F44E"))
		if message.Reaction.count("\U0001F44D") > message.Reaction.count("\U0001F44E"):
			await message.channel.send('The answer is yes')
		else:
			await message.channel.send('The answer is no')
		return

	# sends message when libtard is mentioned
	if 'libtard' in message.content.lower():
		msg = 'libtard epic rekt 8)'.format(message)
		await message.channel.send(msg)
		return

	# sends thinking emoji when someone says hmm
	elif message.content.lower().startswith('hmm'):
		msg = '\U0001F914'.format(message)
		await message.channel.send(msg)
		return

	# sends ben shapiro photo when someone says ok this is epic
	if 'ok this is epic' in message.content.lower() or 'okay this is epic' in message.content.lower():
		msg = ''.format(message)
		await message.channel.send(file=discord.File('my_image.jpg'))
		return

	#credits to haoshaun
	#link to github
	if message.content.lower() == ';details':
		em = discord.Embed(title='read my code!', url='https://github.com/usvimal/Pi-thon', colour=0xb949b5)
		em=em.set_author(name='Minininja',url='https://github.com/usvimal')
		await message.channel.send(embed=em)
		return

	#sends me a message if I am mentioned
	if 'vimal' in message.content.lower():
		msg = message.content.lower().format(message)
		author = message.author
		em = discord.Embed(title='Someone messaged you!', description= msg, colour=0xFF00FF)
		em.set_author(name= author,icon_url=author.avatar_url)
		channel = client.get_user(Vimal)
		await channel.send(embed=em)

token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
