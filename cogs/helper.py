import discord

from discord.ext import commands
from utils.prettydiscordprinter.concrete_printers import PrettyPaginator

class Helper(commands.Cog):
	""" Helper cog for printing out a paginated help message to the users."""
	def __init__(self, bot):
		self._bot = bot
		self._bot.remove_command("help")		# Remove the default help command if this cog is loaded.

	@commands.command()
	async def help(self, ctx, *, entry: str = None):
		""" This help function overrides the default help function. """
		paginator = PrettyPaginator()

		if entry is None:
			await paginator.pretty_print(ctx, [self._create_main_page(ctx)])
		else:
			embed = discord.Embed(title = "Test")
			await ctx.send(self._create_lone_command_help_text(ctx.bot.get_command(entry))[0])

	def _create_main_page(self, ctx):
		""" Create and returns the main page which will show all the command groups and their description. """
		embed = discord.Embed(title="Help: Main Page ")
		embed.description = "Main command groups. Scroll to the next page for more info."

		for name, cog in ctx.bot.cogs.items():
			cog_descript = "No Description"
			if cog.description is not None and cog.description != "":
				cog_descript = cog.description
			embed.add_field(name=name, value=cog_descript, inline=False)

		embed.set_footer(text=f"Created and only usable by {ctx.author.name}")
		return embed

	def _create_command_aliases(self, command):
		" Returns [alias1 or alias2 or alias3] of command. "
		return "[{}]".format(" or ".join([command.name, *command.aliases]))

	def _create_lone_command_help_text(self, command):
		""" Will not attempt to get subcommands of this command but rather return the formatted command usage and
			description.
			Example of command usage: [parent1 or parent 2 or parent 3] [child1 or child2 or child3] <parameter>"""

		self_alias = self._create_command_aliases(command)
		parent_alias = " ".join(reversed([self._create_command_aliases(p) for p in command.parents]))
		if command.usage is None:
			parameter = ""
		else:
			parameter = "<{}>".format(command.usage)

		return "{} {} {}".format(parent_alias, self_alias, parameter), command.help


def setup(bot):
	bot.add_cog(Helper(bot))