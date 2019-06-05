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
			pass

	def _create_main_page(self, ctx):
		embed = discord.Embed(title="Help: Main Page ")
		embed.description = "Main command groups. Scroll to the next page for more info."

		for name, cog in ctx.bot.cogs.items():
			cog_descript = "No Description"
			if cog.description is not None and cog.description != "":
				cog_descript = cog.description
			embed.add_field(name=name, value=cog_descript, inline=False)

		embed.set_footer(text=f"Created and only usable by {ctx.author.name}")
		return embed


def setup(bot):
	bot.add_cog(Helper(bot))