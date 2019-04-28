from discord.ext import commands
import discord

bot = commands.Bot(command_prefix=';', pm_help=None, description='A personal project for fun')

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
		ctx.send(bot.latency)