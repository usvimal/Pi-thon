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

	async def on_message(self, message):
		if message.channel.id == self.channelid:
			await message.add_reaction('✅')
			reactions = (await message.fetch_message(message.id)).reactions
			counts = {}
			for reaction in reactions:
				counts[reaction.emoji] = reaction.count - 1
				print(f'{reaction.emoji} = {counts}')
			if counts['✅'] > 0:
				await message.delete()
				await message.channel.send(strike(message.content))


def setup(bot):
	bot.add_cog(Todo(bot))
