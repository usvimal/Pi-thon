import asyncio
import config
import discord
import logging
import platform
import random
import sys
import traceback

from discord.ext import commands
from utils.db import ensure_todo_table
from utils.discord_handler import DiscordHandler

bot = commands.Bot(command_prefix=config.bot_prefix, pm_help=None, description='A personal project for fun')
logger = logging.getLogger("discord")


@bot.event
# outputs in log when bot is logged in
async def on_ready():
	add_handlers()
	display_startup_message()
	await ensure_todo_table()
	await load_cogs()
	await update_bot_games_frequently()


def add_handlers():
	""" Add Discord and stdout handlers which will output logs to discord and the logging channel and python terminal """
	LOGGING_CHANNEL_ID = 573856996256776202
	logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
	main_loop = bot.loop

	stdout_handler = logging.StreamHandler(sys.stdout)
	discord_handler = DiscordHandler(logging_channel, main_loop, logging.CRITICAL)

	logger.addHandler(stdout_handler)
	logger.addHandler(discord_handler)


def display_startup_message():
	log_in_msg = "Logged in as {} (ID: {}) | Connected to {} servers | Connected to {} users"
	version_msg = "Discord.py Version: {} | Python Version: {}"

	print('=' * 100)
	print("*Hackerman voice* I'm in")
	print(log_in_msg.format(bot.user.name, bot.user.id, len(bot.guilds), len(set(bot.get_all_members()))))
	print(version_msg.format(discord.__version__, platform.python_version()))
	print('=' * 100)


async def load_cogs():
	# Also prints out cogs status on 'pi-thon updates' discord channel.
	loaded_cogs = list()
	failed_cogs = dict()

	for cog in config.cogs:
		try:
			bot.load_extension(cog)
			loaded_cogs.append(cog)
		except Exception as e:
			print(f'Couldn\'t load cog {cog} due to ' + str(e))
			print(traceback.format_exc())
			failed_cogs[cog] = str(e)

	await show_discord_startup_message(loaded_cogs, failed_cogs)


async def show_discord_startup_message(loaded_cogs, failed_cogs):
	if config.show_startup_message == "False":
		return

	channel = bot.get_channel(574240405722234881)

	loaded_cogs_string = "\n".join(loaded_cogs) if len(loaded_cogs) != 0 else "None"
	if len(failed_cogs) != 0:
		failed_cogs_string = "\n".join(f"{name} : {error_name}" for name, error_name in failed_cogs.items())
	else:
		failed_cogs_string = "None"

	em = discord.Embed(title='S T A T U S', description='Pi-thon is up!', colour=0x3c1835)
	em.add_field(name='Loaded cogs', value=loaded_cogs_string, inline=False)
	em.add_field(name='Failed cogs', value=failed_cogs_string, inline=False)
	em.set_author(name='Pi-thon', icon_url=bot.user.avatar_url)

	await channel.send(embed=em)


async def update_bot_games_frequently():
	while True:
		random_game = random.choice(config.games)
		guild_count = len(bot.guilds)
		member_count = len(set(bot.get_all_members()))

		activity_type = random_game[0]
		activity_name = random_game[1].format(guilds=guild_count, members=member_count)
		new_activity = discord.Activity(type=activity_type, name=activity_name)
		await bot.change_presence(activity=new_activity)

		await asyncio.sleep(config.gamestimer)


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
		await message.channel.send(file=discord.File('assets/this_is_epic.jpg'))
		return

	# sends me a message if I am mentioned
	if config.creator in message.content.lower():
		msg = message.content.lower().format(message)
		author = message.author
		guild = message.guild.name
		em = discord.Embed(title='@' + guild, description=msg, colour=0xFF00FF)
		em.set_author(name=author, icon_url=author.avatar_url)
		channel = bot.get_user(config.creatorID)
		await channel.send(embed=em)
		return

	if bot.user.mentioned_in(message):
		await message.add_reaction('👀')


@bot.listen()
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
	if ctx.message.author.id == config.creatorID or ctx.message.author.id == config.CillyID or ctx.message.author.id == config.WYID or ctx.message.author.id == config.MinID:
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

if __name__ == "__main__":
	token = config.DISCORD_BOT_SECRET
	bot.run(token)
