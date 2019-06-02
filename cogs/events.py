import config
import discord

from discord.ext import commands
import utils.checks


class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@staticmethod
	def convert_list_to_string(unconverted_list):
		for i in unconverted_list:
			new_string = ",".join(map(str, unconverted_list))
			return new_string

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if hasattr(ctx.command, 'on_error'):
			return

		if isinstance(error, commands.MissingRequiredArgument):
			return await ctx.send(f"Hol\' up you forgot an argument: {error.param.name}")

		elif isinstance(error, commands.CheckFailure):
			if type(error) == utils.checks.is_officer():
				return await ctx.send("You don't have permission to use this command!")

		elif isinstance(error, commands.BotMissingPermissions):
			return await ctx.send(
				f"I don't have the following permission(s) to run this command!{self.convert_list_to_string(error.missing_perms)}")

		elif isinstance(error, commands.errors.CommandNotFound):
			return

		elif isinstance(error, discord.errors.Forbidden):
			return

		else:
			raise error

	@commands.Cog.listener()
	async def on_message(self, message):
		# we do not want the bot to reply to itself
		if message.author == self.bot.user:
			return

		# sends me a message if I am mentioned
		if config.creator in message.content.lower():
			msg = message.content.lower().format(message)
			author = message.author
			guild = message.guild.name
			em = discord.Embed(title='@' + guild, description=msg, colour=0xFF00FF)
			em.set_author(name=author, icon_url=author.avatar_url)
			channel = self.bot.get_user(config.creatorID)
			await channel.send(embed=em)
			return

		if self.bot.user.mentioned_in(message):
			await message.add_reaction('👀')


@commands.Cog.listener()
async def on_guild_join(self, guild):
	default_prefix = config.default_prefix
	self.bot.all_prefixes[guild.id] = default_prefix
	async with self.bot.dbpool.acquire() as db:
		await db.execute('INSERT INTO guildprop ("guild_id", "prefix") VALUES ($1, $2);',
						guild.id, default_prefix)


@commands.Cog.listener()
async def on_guild_remove(self, guild):
	del self.bot.prefixes[guild.id]
	async with self.bot.dbpool.acquire() as db:
		await db.execute("DELETE FROM guildprop WHERE guild_id=$1", guild.id)


def setup(bot):
	bot.add_cog(Events(bot))
