from discord.ext import commands
import config


class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config

	@commands.guild_only()
	@commands.group()
	async def prefix(self, ctx):
		""" Show current prefix for this guild"""
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed:
				await ctx.send('Oof owie, that was not a valid command 🤨')
			else:
				prefix = self.bot.all_prefixes[ctx.guild.id]
				await ctx.send(f"Current prefix for this server is `{prefix}`.")

	@commands.guild_only()
	@commands.has_permissions(manage_guild=True)
	@prefix.command(aliases=["change"])
	async def set(self, ctx, prefix):
		"""Set guild prefix"""
		guild_id = ctx.guild.id
		if len(prefix) > 5:
			await ctx.send('Please keep your prefix to below 5 characters')
		else:
			if self.bot.all_prefixes.get(ctx.guild.id):
				async with self.bot.dbpool.acquire() as conn:
					await conn.execute(
						'UPDATE guildprop SET "prefix"=$1 WHERE "guild_id"=$2;',
						prefix, guild_id)
			else:
				async with self.bot.dbpool.acquire() as conn:
					await conn.execute(
						'INSERT INTO guildprop ("guild_id", "prefix") VALUES ($1, $2);',
						guild_id, prefix)
			self.bot.all_prefixes[ctx.guild.id] = prefix
			await ctx.send(f"New prefix for this server is `{prefix}`.")

	@commands.group()
	async def brawlhalla(self, ctx):
		"""Enable/Disable Brawlhalla feature"""
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed:
				await ctx.send('Oof owie, that was not a valid command 🤨')
			else:
				if self.bot.brawlhalla_status.get(ctx.author.id):
					await ctx.send('You are subscribed to the brawlhalla down detector')
				else:
					await ctx.send('You are not subscribed to the brawlhalla down detector')

	@brawlhalla.command(aliases=["on"])
	async def enable(self, ctx):
		user_id = ctx.author.id
		if user_id in self.bot.brawlhalla_status:
			async with self.bot.dbpool.acquire() as conn:
				await conn.execute(
					'UPDATE userprop SET "brawlhalla_cog"=$1 WHERE "user_id"=$2;',
					True, user_id)
		else:
			async with self.bot.dbpool.acquire() as conn:
				await conn.execute('INSERT INTO userprop ("user_id", "brawlhalla_cog") VALUES ($1, $2);',
				                   user_id, True)
		self.bot.brawlhalla_status[user_id] = True
		await ctx.message.add_reaction('👍')

	@brawlhalla.command(aliases=["off"])
	async def disable(self, ctx):
		user_id = ctx.author.id
		if user_id in self.bot.brawlhalla_status:
			async with self.bot.dbpool.acquire() as conn:
				await conn.execute(
					'UPDATE userprop SET "brawlhalla_cog"=$1 WHERE "user_id"=$2;',
					False, user_id)
		else:
			async with self.bot.dbpool.acquire() as conn:
				await conn.execute('INSERT INTO userprop ("user_id", "brawlhalla_cog") VALUES ($1, $2);',
				                   user_id, False)
		self.bot.brawlhalla_status[user_id] = False
		await ctx.message.add_reaction('👍')


def setup(bot):
	bot.add_cog(Settings(bot))
