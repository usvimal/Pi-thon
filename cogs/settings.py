import config
import discord

from discord.ext import commands
from utils.lyricsretriever import LyricsRetriever



class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config
		self.lyrics_retriever = LyricsRetriever(bot)

	@commands.guild_only()
	@commands.group()
	async def prefix(self, ctx):
		""" Show current prefix for this guild"""
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed:
				em = discord.Embed(title='Oof! That was not a valid command 🤨 ',
				                   description='Type ;help [command] for more info on a command.',
				                   colour=0x3c1835)
				await ctx.send(embed=em, delete_after=60)
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
			async with self.bot.dbpool.acquire() as conn:
				await conn.execute(
					'UPDATE guildprop SET "prefix"=$1 WHERE "guild_id"=$2;',
					prefix, guild_id)
			self.bot.all_prefixes[ctx.guild.id] = prefix
			await ctx.send(f"New prefix for this server is `{prefix}`.")

	@commands.guild_only()
	@commands.has_permissions(manage_guild=True)
	@prefix.command(aliases=["default"])
	async def reset(self, ctx):
		"""Reset guild prefix"""
		guild_id = ctx.guild.id
		default_prefix = config.default_prefix
		async with self.bot.dbpool.acquire() as conn:
			await conn.execute(
				'UPDATE guildprop SET "prefix"=$1 WHERE "guild_id"=$2;',
				default_prefix, guild_id)
		self.bot.all_prefixes[ctx.guild.id] = default_prefix
		await ctx.send(f"Default prefix set to `{default_prefix}`.")

	@commands.group()
	async def profile(self, ctx):
		"""View status of your settings saved in the bot"""
		current_source = self.lyrics_retriever.get_main_source(ctx.author.id)

		em = discord.Embed(title=f"{ctx.author}'s profile")
		em.set_thumbnail(url=ctx.author.avatar_url)
		em.add_field(name='Lyrics source', value=current_source)
		await ctx.send(embed=em)

	@profile.command(aliases=['del', 'remove'])
	async def delete(self, ctx):
		"""Deletes your information from the server"""
		async with self.bot.dbpool.acquire() as db:
			await db.execute("DELETE FROM userprop WHERE user_id=$1", ctx.author.id)


def setup(bot):
	bot.add_cog(Settings(bot))
