from discord.ext import commands
import config


class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.all_prefixes = {}
		self.brawlhalla_activated = {}
		self.config = config

	@commands.command(aliases=["setprefix"])
	async def prefix(self, ctx, prefix:str):
		"""Set guild prefix"""
		guild_id = ctx.guild.id
		if guild_id is None:
			return
		else:
			if prefix == '':
				self.bot.all_prefixes[ctx.guild.id] = prefix
				await ctx.send(f"Current prefix for this server is `{prefix}`.")
			else:
				if self.bot.all_prefixes.get(ctx.guild.id):
					async with self.bot.dbpool.acquire() as conn:
						await conn.execute(
							'UPDATE guildprop SET "prefix"=$1 WHERE "guild_id"=$2;', prefix, guild_id
						)
				else:
					async with self.bot.dbpool.acquire() as conn:
						await conn.execute(
							'INSERT INTO guildprop ("guild_id", "prefix") VALUES ($1, $2);',
							guild_id,
							prefix
						)
				self.bot.all_prefixes[ctx.guild.id] = prefix
				await ctx.send(f"New prefix for this server is `{prefix}`.")


def setup(bot):
	bot.add_cog(Settings(bot))
