import asyncio
import asyncpg
import config
import discord
import importlib
import jishaku
import json
import logging
import platform
import random
import sys
import traceback
import urllib.request

from discord.ext import commands
from utils.db import Database
from utils.discord_handler import DiscordWriter


class MainBot(commands.Bot):
	LOGGING_CHANNEL_ID = 573856996256776202
	UPDATES_CHANNEL_ID = 574240405722234881
	bot_requirements = {
		'jishaku': 'jishaku',
		'lyricsgenius': 'lyricsgenius',
		'discord': 'discord.py',
		'owotrans': 'owotranslator',
		'psutil': 'psutil',
		'pylyrics3': 'pylyrics3',
		'urllib3': 'urllib3',
		'asyncpg': 'asyncpg',
		'bs4': 'beautifulsoup4'
	}

	def __init__(self, *args, **kwargs):
		super().__init__(command_prefix=self._get_prefix, **kwargs)

		self._logging_channel = None
		self._updates_channel = None
		self.all_prefixes = {}
		self.brawlhalla_status = {}
		self.lyrics_source = {}

	async def on_ready(self):
		self._logging_channel = self.get_channel(self.LOGGING_CHANNEL_ID)
		self._updates_channel = self.get_channel(self.UPDATES_CHANNEL_ID)

		self._add_handlers()
		self._display_startup_message()
		await self.init_postgres_connection()
		self.database = Database(main_loop=self.loop, bot=self)
		await self.batch_fetch_from_db()
		await self._load_cogs()
		await self.check_packages(self.bot_requirements)
		await self._update_bot_games_frequently() #this must be the last

	def _add_handlers(self):
		""" Change stdout and stderr to also print out to discord. Outputs and errors will still be printed to console. """
		sys.tracebacklimit = 0			# Reduce traceback stack size to 0
		sys.stdout = DiscordWriter(sys.stdout, self._logging_channel)
		sys.stderr = DiscordWriter(sys.stderr, self._logging_channel)

	def _display_startup_message(self):
		log_in_msg = "Logged in as {} (ID: {}) | Connected to {} servers | Connected to {} users"
		version_msg = "Discord.py Version: {} | Python Version: {}"

		print('=' * 100)
		print("*Hackerman voice* I'm in")
		print(log_in_msg.format(self.user.name, self.user.id, len(self.guilds), len(set(self.get_all_members()))))
		print(version_msg.format(discord.__version__, platform.python_version()))
		print('=' * 100)

	async def _load_cogs(self):
		# Also prints out cogs status on 'pi-thon updates' discord channel.
		loaded_cogs = list()
		failed_cogs = dict()

		for cog in config.cogs:
			try:
				self.load_extension(cog)
				loaded_cogs.append(cog)
			except Exception as e:
				print(f'Couldn\'t load cog {cog} due to ' + str(e))
				print(traceback.format_exc())
				failed_cogs[cog] = str(e)

		await self._show_discord_startup_message(loaded_cogs, failed_cogs)

	async def _show_discord_startup_message(self, loaded_cogs, failed_cogs):
		if config.show_startup_message == "False":
			return

		loaded_cogs_string = "\n".join(loaded_cogs) if len(loaded_cogs) != 0 else "None"
		if len(failed_cogs) != 0:
			failed_cogs_string = "\n".join(f"{name} : {error_name}" for name, error_name in failed_cogs.items())
		else:
			failed_cogs_string = "None"

		em = discord.Embed(title='S T A T U S', description='Pi-thon is up!', colour=0x3c1835)
		em.add_field(name='Loaded cogs', value=loaded_cogs_string, inline=False)
		em.add_field(name='Failed cogs', value=failed_cogs_string, inline=False)
		em.set_author(name='Pi-thon', icon_url=self.user.avatar_url)

		await self._updates_channel.send(embed=em)

	async def _update_bot_games_frequently(self):
		while True:
			random_game = random.choice(config.games)
			guild_count = len(self.guilds)
			member_count = len(set(self.get_all_members()))

			activity_type = random_game[0]
			activity_name = random_game[1].format(guilds=guild_count, members=member_count)
			new_activity = discord.Activity(type=activity_type, name=activity_name)
			await self.change_presence(activity=new_activity)

			await asyncio.sleep(config.gamestimer)

	async def init_postgres_connection(self):
		self.dbpool = await asyncpg.create_pool(dsn=config.DATABASE_URL)

	async def batch_fetch_from_db(self):
		async with self.dbpool.acquire() as conn:
			await self.fetch_prefixes_from_db(conn)
			await self.fetch_brawlhalla_status_from_db(conn)
			await self.fetch_lyrics_source_from_db(conn)

	async def fetch_prefixes_from_db(self, connection):
		prefixes = await connection.fetch("SELECT guild_id, prefix FROM guildprop;")
		for row in prefixes:
			self.all_prefixes[row["guild_id"]] = row["prefix"]

	def _get_prefix(self, bot, message):
		if not message.guild:
			return config.default_prefix  # Use default prefix in DMs
		try:
			return commands.when_mentioned_or(self.all_prefixes[message.guild.id])(self, message)
		except KeyError:
			return commands.when_mentioned_or(config.default_prefix)(self, message)

	async def fetch_brawlhalla_status_from_db(self, connection):
		brawlhalla_status = await connection.fetch("SELECT user_id, brawlhalla_cog FROM userprop;")
		for row in brawlhalla_status:
			self.brawlhalla_status[row["user_id"]] = row["brawlhalla_cog"]

	async def fetch_lyrics_source_from_db(self, connection):
		lyrics_source = await connection.fetch("SELECT user_id, lyrics_source FROM userprop;")
		for row in lyrics_source:
			self.lyrics_source[row["user_id"]] = row["lyrics_source"]

	async def is_owner(self, user: discord.User):
		if user.id == config.MinID or user.id == config.creatorID:  # Implement your own conditions here
			return True
		return False

	async def check_packages(self, package_dict):
		latest_version = {}
		for package_name, online_name in package_dict.items():
			mod = importlib.import_module(package_name)
			data = urllib.request.urlopen("https://www.pypi.org/pypi/" + online_name + "/json").read()
			output = json.loads(data)
			version_no = output['info']['version']
			online_version = version_no[0:6]
			try:
				current_version = mod.__version__
				if current_version != online_version:
					latest_version[package_name] = online_version
			except Exception as e:
				print('Error retrieving info on', package_name, 'Reason:', e,
				      '\nPlease fix the dictionary items or remove them.')
		if latest_version:
			await self._updates_channel.send('The following modules have updates:' + str(latest_version))


if __name__ == "__main__":
	bot = MainBot(pm_help=None, description='A personal project for fun')
	token = config.DISCORD_BOT_SECRET
	bot.run(token)
