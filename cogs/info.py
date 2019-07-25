import aiohttp
import discord
import os
import platform
import psutil
import requests
import time

from bs4 import BeautifulSoup
from discord.ext import commands


class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.feedback_channel = bot.get_channel(584041570739945502)

	@commands.command(aliases=["code"])
	async def github(self, ctx):
		"""link to github"""
		em = discord.Embed(title='read my code!', url='https://github.com/usvimal/Pi-thon', colour=0xb949b5)
		em = em.set_author(name='Minininja', url='https://github.com/usvimal')
		await ctx.send(embed=em)
		return

	@commands.command(aliases=["latency"])
	async def ping(self, ctx):
		"""check ping"""
		pingtime = time.time()
		async with ctx.typing():
			ping = float(format(time.time() - pingtime, '.03f'))
		await ctx.send(f" time is `{ping} seconds` :ping_pong:")
		return

	@commands.command()
	async def link(self, ctx):
		"""link to add bot to other servers"""
		await ctx.send(
			'https://discordapp.com/api/oauth2/authorize?client_id=517153107604668438&permissions=0&scope=bot')

	@commands.command()
	async def feedback(self, ctx, *, content):
		"""Send feedback to bot developer"""
		em = discord.Embed(title='Feedback', colour=0x37d9b9)
		em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
		em.description = content
		em.timestamp = ctx.message.created_at

		if ctx.guild is not None:
			em.add_field(name='Server', value=f'{ctx.guild.name} (ID: {ctx.guild.id})', inline=False)
			em.add_field(name='Channel', value=f'{ctx.channel} (ID: {ctx.channel.id})', inline=False)
		em.set_footer(text=f'Author ID: {ctx.author.id}')

		await self.feedback_channel.send(embed=em)
		await ctx.message.add_reaction('👍')

	@commands.command()
	@commands.is_owner()
	async def dm(self, ctx, user_id: int, *, content: str):
		"""Dm a user with their id"""
		user = self.bot.get_user(user_id)
		em = discord.Embed(title='Feedback reply', description=content)
		em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		em.set_footer(text='This is a DM sent because you had previously requested feedback or I found a bug '
		                   'in a command you used, I do not monitor this DM.')
		try:
			await user.send(embed=em)
		except:
			await ctx.send(f'Could not PM user by ID {user_id}.')
		else:
			await ctx.message.add_reaction('👍')

	@commands.command(aliases=["status"])
	async def info(self, ctx):
		"""Bot status"""
		appinfo = await self.bot.application_info()
		process = psutil.Process(os.getpid())
		mem_usage = round(process.memory_info().rss / 1048576, 1)
		url = 'https://github.com/usvimal/Pi-thon/commits/rewrite-v2.0'
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				if response.status == 200:
					text = await response.read()
					soup = BeautifulSoup(text, "html.parser")
		last_commit_image = soup.find('a', class_="commit-author tooltipped tooltipped-s user-mention")
		last_commit = last_commit_image.find_previous('a').find_previous('a')
		changelog = last_commit.contents[0]

		em = discord.Embed(title=f"Bot Info for {appinfo.name}",
		                   description=f"[Bot Invite](https://discordapp.com/oauth2/authorize?&client_id={self.bot.user.id}&scope=bot&permissions=0) | [Source Code](https://github.com/usvimal/Pi-thon)")
		em.add_field(name='Guilds', value=str(len(self.bot.guilds)))
		em.add_field(name="Users", value=str(len(self.bot.users)))
		em.add_field(name="Mem usage", value=f'{mem_usage} MiB')
		em.add_field(name="CPU usage", value=f'{psutil.cpu_percent()}%')
		em.add_field(name="Guild prefix", value=f"``{ctx.prefix}``")
		em.add_field(name='Bot owners', value=f'{appinfo.owner} \nmk43v3r#1422')
		em.add_field(name='Latest commit', value=f'`[{changelog}](https://github.com/usvimal/Pi-thon/commits/rewrite-v2.0)`')
		em.set_footer(text=f'Python version: {platform.python_version()} , discord.py version: {discord.__version__}')
		await ctx.send(embed=em)


def setup(bot):
	bot.add_cog(Info(bot))
