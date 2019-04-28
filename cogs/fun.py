from discord.ext import commands
import owotrans

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def owo(self, ctx, *, arg):
		msg = owotrans.owo(arg)
		await ctx.send(msg)
