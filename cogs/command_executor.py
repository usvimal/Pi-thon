import asyncio
import discord
import sys

from discord.ext import commands
from io import StringIO


class CommandExecutor(commands.Cog):
	""" Execute code dynamically in discord and show output and error """
	def __init__(self, bot):
		pass

	@commands.group()
	def cmd(self, ctx):
		pass

	@cmd.command()
	def execute(self, ctx, *, args):
		# set standard system output and error to these 2 file-like strings temporarily
		code_out, code_err = StringIO(), StringIO()
		sys.stdout, sys.stderr = code_out, code_err

		exec(args)

		em = discord.Embed(title='Command Executor', description='I execute commands.')
		em.add_field(name='Output', value=code_out.getvalue(), inline=False)
		em.add_field(name='Errors', value=code_err.getvalue(), inline=False)

		async with ctx.typing():
			await ctx.send(embed=em)

		# restore stdout and stderr
		sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__

		code_out.close()
		code_err.close()


def setup(bot):
	bot.add_cog(CommandExecutor(bot))


if __name__ == "__main__":
	pass