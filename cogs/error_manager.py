from discord.ext import commands
import utils.checks


class ErrorManager(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@staticmethod
	def convert_list_to_string(unconverted_list):
		for i in unconverted_list:
			new_string = ",".join(map(str, unconverted_list))
			return new_string

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			return await ctx.send(f"Hol\' up you forgot an argument: {error.param.name}")

		elif isinstance(error, commands.CheckFailure):
			if type(error) == utils.checks.is_officer():
				return await ctx.send("You don't have permission to use this command!")

		elif isinstance(error, commands.BotMissingPermissions):
			return await ctx.send(
				f"I don't have the following permission(s) to run this command!{self.convert_list_to_string(error.missing_perms)}")


def setup(bot):
	bot.add_cog(ErrorManager(bot))
