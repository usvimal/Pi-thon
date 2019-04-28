from discord.ext import commands
import discord
import time

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=["code", "github"])
	async def details(self, ctx):
		"""link to github"""
		em = discord.Embed(title='read my code!', url='https://github.com/usvimal/Pi-thon', colour=0xb949b5)
		em = em.set_author(name='Minininja', url='https://github.com/usvimal')
		await ctx.send(embed=em)
		return

	@commands.command(aliases=["latency"])
	async def ping(self,ctx):
		"""check ping"""
		pingtime = time.time()
		async with ctx.typing():
			ping = float(format(time.time() - pingtime, '.03f'))
		await ctx.send(f" time is `{ping} seconds` :ping_pong:")
		return

	@commands.command()
	async def link(self,ctx):
		"""link to add bot to other servers"""
		await ctx.send('https://discordapp.com/api/oauth2/authorize?client_id=517153107604668438&permissions=0&scope=bot')


def setup(bot):
	bot.add_cog(Info(bot))
