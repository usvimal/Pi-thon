import discord

from discord.ext import commands
from utils.text_formatter import strike


class Todo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.todo_channel_id = 572561960982413334

	@commands.is_owner()
	@commands.command()
	async def task(self, ctx, *, arg: commands.clean_content(fix_channel_mentions=True)):
		"""Add task to todo channel"""
		channel = self.bot.get_channel(self.todo_channel_id)
		em = discord.Embed(description=arg)
		em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		em.timestamp = ctx.message.created_at
		task = await channel.send(embed=em)
		await task.add_reaction('✅')
		await task.add_reaction('❌')

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		try:
			channel = self.bot.get_channel(payload.channel_id)
			message = await channel.fetch_message(payload.message_id)
		except:
			return
		else:
			emoji = payload.emoji
			user = message.guild.get_member(payload.user_id)

			if user == self.bot.user or payload.channel_id != self.todo_channel_id:
				return
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
					striked_message = strike(embed.description)
					author_image = embed.author.icon_url
					author = embed.author.name
					await message.delete()
					em = discord.Embed(title=striked_message)
					em.set_author(name=author, icon_url=author_image)
					em.timestamp = message.created_at
					await channel.send(embed=em)
				if str(emoji) == '❌':
					await message.delete()


def setup(bot):
	bot.add_cog(Todo(bot))
