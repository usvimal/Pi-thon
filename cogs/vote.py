import asyncio
from discord.ext import commands


class Vote(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def vote(self, ctx, *, question: str):
		"""vote feature, will add reactions (thumbsup and thumbsdown) and output final result"""
		"""enter time in seconds and your reason"""
		await ctx.message.add_reaction('✅')
		await ctx.message.add_reaction('❌')
		await ctx.send("How long do you want the vote to run? (in seconds)")

		def check(user):
			return user == ctx.author
		try:
			msg = await self.bot.wait_for("message", timeout=60.0, check=check)
			print(msg.content)
		except asyncio.TimeoutError:
			await ctx.send('The vote has been cancelled due to a lack of response')
		else:
			if msg.content.isdigit():
				await ctx.send('👍 vote is running')
				await asyncio.sleep(int(msg.content))
			else:
				await ctx.send('Please restart the vote and send a positive integer only')
				return
			reactions = (await ctx.fetch_message(ctx.message.id)).reactions
			print(reactions)
			counts = {}
			for reaction in reactions:
				counts[reaction.emoji] = reaction.count - 1
				print(f'{reaction.emoji} = {counts}')
			if counts['✅'] > counts['❌']:
				await ctx.send('The answer to ' + question + ' is: ✅')
			elif counts['✅'] < counts['❌']:
				await ctx.send('The answer to ' + question + ' is: ❌')
			else:
				await ctx.send('Aww shucks, its a stalemate')
				return
			return


def setup(bot):
	bot.add_cog(Vote(bot))
