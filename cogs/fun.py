import owotrans
from discord.ext import commands


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def owo(self, ctx, *, arg):
		"""owoifies your message"""
		msg = owotrans.owo(arg)
		await ctx.send(msg)


def setup(bot):
	bot.add_cog(Fun(bot))
