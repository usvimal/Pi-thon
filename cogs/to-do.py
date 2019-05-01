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
		self.message = bot.message

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.channel.id == self.channelid:
			await message.add_reaction('✅')
			await message.add_reaction('❌')

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, reaction):
		if self.message.channel.id == self.channelid:
			if reaction == '✅':
				await self.message.delete()
				await self.message.channel.send(strike(self.message.content))
			if reaction == '❌':
				await self.message.delete()



def setup(bot):
	bot.add_cog(Todo(bot))
