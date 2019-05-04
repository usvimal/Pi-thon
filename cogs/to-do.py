from discord.ext import commands


def strike(text):
	result = ''
	for c in text:
		result = result + c + '\u0336'
	return result


class Todo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.todo_channel_id = 572561960982413334

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return

		if message.channel.id == self.todo_channel_id:
			await message.add_reaction('✅')
			await message.add_reaction('❌')

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
