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

	@commands.command()
	async def execute(self, ctx, *, arg):
		"""Enter Python code to execute it"""
		try:
			exec(arg)
		except Exception as e:
			await ctx.send('Something went wrong... Please check your code. \n Output:' + str(e))


def setup(bot):
	bot.add_cog(Fun(bot))
