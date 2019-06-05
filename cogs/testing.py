from discord.ext import commands


class Testing(commands.Cog):
	""" Testing cog for trying out experimental code. """
	def __init__(self, bot):
		self._bot = bot

	@commands.is_owner()
	@commands.command()
	async def poke_testing(self, ctx):
		""" Utility function to check testing cog is active. """
		command_names = " | ".join(c.name for c in self.get_commands())
		await ctx.send(f"`Testing cog active. Test commands = {command_names}`")

	@commands.is_owner()
	@commands.command()
	async def test_get_command(self, ctx, *, arg):
		""" Test bot.get_command(command_name)"""
		await ctx.send(ctx.bot.get_command(arg).help)

	@commands.is_owner()
	@commands.command()
	async def test_walk_commands(self, ctx, *, arg):
		""" Test cog.walk_commands()"""
		for c in ctx.bot.get_cog(arg).walk_commands():
			await ctx.send(c.help)

	@commands.is_owner()
	@commands.command()
	async def test_bot_cogs(self, ctx, *, arg):
		""" Test bot.cogs"""
		for cog_name, cog_instance in ctx.bot.cogs.items():
			description = "No description"
			if cog_instance.description is not None and cog_instance.description != "":
				description = cog_instance.description

			await ctx.send(f"{cog_name}, {description}")

def setup(bot):
	bot.add_cog(Testing(bot))