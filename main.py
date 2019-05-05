import discord
import os
import platform
import asyncio
import time
import asyncpg
import random
from discord.ext import commands
import owotrans
import lyricsgenius
import loadconfig
import logging
import traceback
import time
from discord_handler import DiscordHandler

bot = commands.Bot(command_prefix=';', pm_help=None, description='A personal project for fun')
logger = logging.getLogger("discord")


def _add_discord_handler():
	LOGGING_CHANNEL_ID = 573856996256776202
	logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
	main_loop = bot.loop
	print(logging_channel, main_loop)		# For tracing

	handler = DiscordHandler(logging_channel, main_loop, logging.CRITICAL)

	logger.addHandler(handler)


@bot.event
# outputs in log when bot is logged in
async def on_ready():
	_add_discord_handler()
	print("*Hackerman voice* I'm in")
	print('Logged in as ' + str(bot.user.name) + ' (ID:' + str(bot.user.id) + ') | Connected to ' + str(
		len(bot.guilds)) + ' servers | Connected to ' + str(len(set(bot.get_all_members()))) + ' users')
	print('--------')
	print('Discord.py Version:{} | Python Version: {}'.format(discord.__version__, platform.python_version()))
	failed_cogs = list()
	for cog in loadconfig.cogs:
		try:
			bot.load_extension(cog)
		except Exception as e:
			print(f'Couldn\'t load cog {cog} due to ' + str(e))
			print(traceback.format_exc())
			failed_cogs.append(cog)

	if failed_cogs != '[]':
		failed_cogs_value = ",".join(failed_cogs)
	else:
		failed_cogs_value = 'None'

	channel = bot.get_channel(574240405722234881)
	loaded_cogs = None
	for key in bot.extensions:
		loaded_cogs_list = list(bot.extensions.keys())
		loaded_cogs = ','.join(loaded_cogs_list)

	em = discord.Embed(title='S T A T U S', description='Pi-thon is up!', colour=0x3c1835)
	em.add_field(name='Loaded cogs', value=loaded_cogs, inline=False)
	em.add_field(name='Failed cogs', value=failed_cogs_value, inline=False)
	em.set_author(name='Pi-thon', icon_url=bot.user.avatar_url)
	await channel.send(embed=em)

	while True:
		randomGame = random.choice(loadconfig.games)
		guild_count = str(len(bot.guilds))
		member_count = str(len(set(bot.get_all_members())))
		await bot.change_presence(activity=discord.Activity(type=randomGame[0], name=randomGame[1].format(guilds = guild_count, members = member_count)))
		await asyncio.sleep(loadconfig.gamestimer)


@bot.listen()
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == bot.user:
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
		await message.channel.send(file=discord.File('this_is_epic.jpg'))
		return

	# sends me a message if I am mentioned
	if loadconfig.creator in message.content.lower():
		msg = message.content.lower().format(message)
		author = message.author
		guild = message.guild.name
		em = discord.Embed(title='@' + guild, description=msg, colour=0xFF00FF)
		em.set_author(name=author, icon_url=author.avatar_url)
		channel = bot.get_user(loadconfig.creatorID)
		await channel.send(embed=em)
		return

	if bot.user.mentioned_in(message):
		await message.add_reaction('👀')


@bot.listen
async def on_member_update(before, after):
	if before.avatar != after.avatar:
		# gets the first channel from UI
		ctx = before.guild.text_channels[0]
		await ctx.send(f'Ayy nice new dp! {before.mention}')


@bot.command()
async def talk(ctx, *, arg):
	"""deletes your message and talks through the bot"""
	await ctx.message.delete()
	print(ctx.message.author.id)
	if ctx.message.author.id == loadconfig.creatorID or ctx.message.author.id == loadconfig.CillyID or ctx.message.author.id == loadconfig.WYID or ctx.message.author.id == loadconfig.MinID:
		await ctx.send(arg)
		return
	else:
		await ctx.send(f'You are not authorised sorry! {ctx.author.mention}')
		return


@bot.command()
async def log(ctx, *, arg):
	arg = arg.lower()
	if arg == "debug":
		logger.debug("Debug")
	elif arg == "info":
		logger.info("Info")
	elif arg == "warning":
		logger.warning("Warning")
	elif arg == "error":
		logger.error("Error")
	elif arg == "critical":
		logger.critical("Critical")

token = loadconfig.discord_key
bot.run(token)
