import asyncio
import asyncpg
import config
import discord
import logging
import platform
import random
import sys
import traceback

from discord.ext import commands
# 	from utils.db import ensure_todo_table
from utils.discord_handler import DiscordHandler


logger = logging.getLogger("discord")


class MainBot(commands.Bot):
	LOGGING_CHANNEL_ID = 573856996256776202
	UPDATES_CHANNEL_ID = 574240405722234881

	def __init__(self, *args, **kwargs):
		super().__init__(command_prefix=self._get_prefix, **kwargs)

		self._logging_channel = None
		self._updates_channel = None
		self.all_prefixes = {}

	async def on_ready(self):
		self._logging_channel = self.get_channel(self.LOGGING_CHANNEL_ID)
		self._updates_channel = self.get_channel(self.UPDATES_CHANNEL_ID)

		self._add_handlers()
		self._display_startup_message()
		await self.init_postgres_connection()
		# await ensure_todo_table()
		await self._load_cogs()
		await self._update_bot_games_frequently()

	def _add_handlers(self):
		""" Add Discord and stdout handlers which will output logs to discord and the logging channel and python terminal """
		stdout_handler = logging.StreamHandler(sys.stdout)
		discord_handler = DiscordHandler(self._logging_channel, self.loop, logging.CRITICAL)

		logger.addHandler(stdout_handler)
		logger.addHandler(discord_handler)

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

		async with self.dbpool.acquire() as conn:
			prefixes = await conn.fetch("SELECT guild_id, prefix FROM guildprop;")
			for row in prefixes:
				self.all_prefixes[row["guild_id"]] = row["prefix"]

	def _get_prefix(self, message):
		if not message.guild:
			return config.default_prefix  # Use default prefix in DMs
		try:
			return commands.when_mentioned_or(self.all_prefixes[message.guild.id])(self, message)
		except KeyError:
			return commands.when_mentioned_or(config.default_prefix)(self, message)

	async def on_message(self, message):
		# we do not want the bot to reply to itself
		a = await self.get_prefix(message)
		if message.author == self.user:
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
			channel = self.get_user(config.creatorID)
			await channel.send(embed=em)
			return

		if self.user.mentioned_in(message):
			await message.add_reaction('👀')

		await bot.process_commands(message)

	@staticmethod
	async def on_member_update(before, after):
		if before.avatar != after.avatar:
			# gets the first channel from UI
			ctx = before.guild.text_channels[0]
			await ctx.send(f'Ayy nice new dp! {before.mention}')


if __name__ == "__main__":
	bot = MainBot(pm_help=None, description='A personal project for fun')
	token = config.DISCORD_BOT_SECRET
	bot.run(token)
