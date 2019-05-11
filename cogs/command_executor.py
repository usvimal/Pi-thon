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
	async def cmd(self, ctx):
		pass

	@cmd.command()
	async def execute(self, ctx, *, args):
		# set standard system output and error to these 2 file-like strings temporarily
		code_out, code_err = StringIO(), StringIO()
		old_out, old_err = sys.stdout, sys.stderr
		sys.stdout, sys.stderr = code_out, code_err

		exec(args)

		# restore stdout and stderr
		sys.stdout, sys.stderr = old_out, old_err
		v1, v2 = code_out.getvalue(), code_err.getvalue()

		output_str = v1 if len(v1) > 0 else "None"
		err_str = v2 if len(v2) > 0 else "None"

		em = discord.Embed(title='Command Executor', description='I execute commands.')
		em.add_field(name='Output', value=output_str, inline=False)
		em.add_field(name='Errors', value=err_str, inline=False)

		async with ctx.typing():
			await ctx.send(embed=em)

		code_out.close()
		code_err.close()


def setup(bot):
	bot.add_cog(CommandExecutor(bot))


if __name__ == "__main__":
	pass