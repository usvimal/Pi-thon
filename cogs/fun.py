import config
import owotrans

from discord.ext import commands
from utils.checks import is_approved_talker


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def owo(self, ctx, *, arg):
		"""owoifies your message"""
		msg = owotrans.owo(arg)
		await ctx.send(msg)

	@commands.command(aliases=["say"])
	@is_approved_talker()
	@commands.bot_has_permissions(manage_messages=True)
	async def talk(self, ctx, *, arg):
		"""deletes your message and talks through the bot"""
		await ctx.message.delete()
		await ctx.send(arg)


def setup(bot):
	bot.add_cog(Fun(bot))
