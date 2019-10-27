import config
import discord

from discord.ext import commands


class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		# If command has its own error handler, don't do anything
		if hasattr(ctx.command, 'on_error'):
			return

		# Get error.original if it is not the original error
		error = getattr(error, "original", error)

		ignored_errors = (commands.errors.CommandNotFound,
							commands.errors.TooManyArguments,
							discord.errors.NotFound,
							discord.errors.Forbidden)

		if isinstance(error, ignored_errors):
			return

		elif isinstance(error, commands.CheckFailure):
			await ctx.send(str(error))

		elif isinstance(error, commands.MissingRequiredArgument):
			return await ctx.send(f"Hol\' up you forgot an argument: {error.param.name}")

		elif isinstance(error, commands.BadArgument):
			return await ctx.send(f'Uh oh there was an error: {error}')

		else:
			# Decorate the error message with the source guild and source user.
			invoker = f" | Source Channel: {ctx.guild.name} | Source User: {ctx.author.name} | Invoked command: {ctx.command}"
			error.args = (error.args[0] + invoker, )

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

		if config.nword1 or config.nword2 in message.content.lower():
			if config.nword1 in message.content.lower():
				user_id = message.author.id
				if user_id in self.bot.nword1_counter or self.bot.nword2_counter:
					async with self.bot.dbpool.acquire() as conn:
						nword1 = self.bot.nword1_counter.get(user_id)
						nword1 += 1
						await conn.execute(
							'UPDATE nwordtable SET "nword1"=$1 WHERE "user_id"=$2;',
							nword1, user_id)
						self.bot.nword1_counter[user_id] = nword1
				else:
					async with self.bot.dbpool.acquire() as conn:
						await conn.execute('INSERT INTO nwordtable ("user_id", "nword1") VALUES ($1, $2);',
						                   user_id, 1)
						self.bot.nword1_counter[user_id] = 1

			if config.nword2 in message.content.lower():
				user_id = message.author.id
				if user_id in self.bot.nword1_counter or self.bot.nword2_counter:
					async with self.bot.dbpool.acquire() as conn:
						nword2 = self.bot.nword2_counter.get(user_id)
						nword2 += 1
						await conn.execute(
							'UPDATE nwordtable SET "nword2"=$1 WHERE "user_id"=$2;',
							nword2, user_id)
						self.bot.nword2_counter[user_id] = nword2
				else:
					async with self.bot.dbpool.acquire() as conn:
						await conn.execute('INSERT INTO nwordtable ("user_id", "nword2") VALUES ($1, $2);',
						                   user_id, 1)
						self.bot.nword2_counter[user_id] = 1

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		default_prefix = config.default_prefix
		self.bot.all_prefixes[guild.id] = default_prefix
		async with self.bot.dbpool.acquire() as db:
			await db.execute('INSERT INTO guildprop ("guild_id", "prefix") VALUES ($1, $2);',
							guild.id, default_prefix)

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		del self.bot.all_prefixes[guild.id]
		async with self.bot.dbpool.acquire() as db:
			await db.execute("DELETE FROM guildprop WHERE guild_id=$1", guild.id)


def setup(bot):
	bot.add_cog(Events(bot))
