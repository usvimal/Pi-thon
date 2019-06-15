import asyncio

from discord.ext import commands


class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	@commands.command(aliases=["purge"])
	async def clean(self, ctx, *, limit: int):
		await ctx.message.channel.purge(limit=limit + 1)  # also deletes your own message
		deletion_message = await ctx.send(f"`{limit}` messages were deleted")
		await asyncio.sleep(10)
		await deletion_message.delete()


def setup(bot):
	bot.add_cog(Moderation(bot))
