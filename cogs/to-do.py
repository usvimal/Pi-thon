from discord.ext import commands


def strike(text):
	result = ''
	for c in text:
		result = result + c + '\u0336'
	return result


class Todo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.channelid = 572561960982413334

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.channel.id == self.channelid:
			await message.add_reaction('✅')
			await message.add_reaction('❌')

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, message_id, channel_id, emoji):
		if channel_id == self.channelid:
			if emoji == '✅':
				await message_id.delete()
				await channel_id.send(strike(message_id.content))
			if emoji == '❌':
				await message_id.delete()


def setup(bot):
	bot.add_cog(Todo(bot))
