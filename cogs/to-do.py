import discord

from discord.ext import commands
from utils import checks
from utils.text_formatter import strike


class Todo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.todo_channel_id = 572561960982413334

	@checks.is_officer()
	@commands.command()
	async def task(self, ctx, *, arg):
		"""Add task to todo channel"""
		channel = self.bot.get_channel(self.todo_channel_id)
		em = discord.Embed(title=arg)
		em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		task = await channel.send(embed=em)
		await task.add_reaction('✅')
		await task.add_reaction('❌')

	@checks.in_hideout_task_channel()
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		channel = self.bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		emoji = payload.emoji
		user = message.guild.get_member(payload.user_id)

		try:
			embed = message.embeds[0]
		except:
			if str(emoji) == '✅':
				await message.delete()
				await channel.send(strike(message.content))
			if str(emoji) == '❌':
				await message.delete()
		else:
			if str(emoji) == '✅':
				striked_message = strike(embed['title'])
				author_image = embed['thumbnail']['url']
				author = embed['author']
				await message.delete()
				em = discord.Embed(title=striked_message)
				em.set_author(name=author,icon_url=author_image)
				channel.send(embed=em)
			if str(emoji) == '❌':
				await message.delete()


def setup(bot):
	bot.add_cog(Todo(bot))
