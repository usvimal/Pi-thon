from discord.ext import commands
from utils import checks
from utils.text_formatter import strike


class Todo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.todo_channel_id = 572561960982413334

	@checks.is_officer()
	@commands.command()
	async def task(self, ctx):
		"""Add task to todo channel"""
		channel = self.bot.get_channel(self.todo_channel_id)
		task = await channel.send(ctx.message.content)
		await task.add_reaction('✅')
		await task.add_reaction('❌')

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		channel = self.bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		emoji = payload.emoji
		user = message.guild.get_member(payload.user_id)

		if user == self.bot.user:
			return

		if payload.channel_id == self.todo_channel_id:
			if str(emoji) == '✅':
				await message.delete()
				await channel.send(strike(message.content))
			if str(emoji) == '❌':
				await message.delete()


def setup(bot):
	bot.add_cog(Todo(bot))
