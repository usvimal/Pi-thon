import owotrans
from discord.ext import commands
import config


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def owo(self, ctx, *, arg):
		"""owoifies your message"""
		msg = owotrans.owo(arg)
		await ctx.send(msg)

	@commands.command()
	@commands.bot_has_permissions(manage_messages=True)
	async def talk(self, ctx, *, arg):
		"""deletes your message and talks through the bot"""
		await ctx.message.delete()
		print(ctx.message.author.id)
		if ctx.message.author.id == config.creatorID or ctx.message.author.id == config.CillyID or ctx.message.author.id == config.WYID or ctx.message.author.id == config.MinID:
			await ctx.send(arg)
			return
		else:
			await ctx.send(f'You are not authorised sorry! {ctx.author.mention}')
			return

def setup(bot):
	bot.add_cog(Fun(bot))
