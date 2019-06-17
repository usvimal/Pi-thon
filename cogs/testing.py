import discord

from discord.ext import commands


class Testing(commands.Cog):
	""" Testing cog for trying out experimental code. """
	def __init__(self, bot):
		self._bot = bot

	@commands.is_owner()
	@commands.command(hidden=True)
	async def poke_testing(self, ctx):
		""" Utility function to check testing cog is active. """
		command_names = " | ".join(c.name for c in self.get_commands())
		await ctx.send(f"`Testing cog active. Test commands = {command_names}`")

	@commands.is_owner()
	@commands.command(hidden=True)
	async def raise_error(self, ctx, *, args):
		""" Used to raise specific errors for the purpose of testing the error handler. """
		class DummyResponse:
			def __init__(self):
				self.status = None
				self.reason = None

		if args == "a":
			raise discord.Forbidden(DummyResponse(), "")
		elif args == "b":
			raise discord.NotFound(DummyResponse(), "")
		elif args == "c":
			raise discord.errors.NotFound(DummyResponse(), "")
		elif args == "d":
			raise discord.errors.Forbidden(DummyResponse(), "")


def setup(bot):
	bot.add_cog(Testing(bot))