import asyncio
import discord
import sys
import traceback

from utils.text_formatter import chunks
from discord.ext import commands
from io import StringIO
from utils import checks


class CommandExecutor(commands.Cog):
	""" Execute code dynamically in discord and show output and error """
	def __init__(self, bot):
		self._variables = dict()
		self._mute = False

	@commands.group()
	@checks.is_officer()
	async def cmd(self, ctx):
		""" Shows the status of the command executor. """
		if ctx.invoked_subcommand is None:
			if len(self._variables) > 0:
				s = self.get_printable_variables()
			else:
				s = "None"
			for c in chunks(s, 2048):
				embed = discord.Embed(title="Command Executor", description=f"mute = {self._mute}")
				embed.add_field(name="Local variables", value=c, inline=False)
				async with ctx.typing():
					await ctx.send(embed=embed)

	def get_printable_variables(self):
		""" Change to a format where every value is printed line by line and shrinked if it exceeds the line limit."""
		if len(self._variables) > 0:
			formatted_vars = [self.get_shrinked_variables(name, value) for name, value in self._variables.items()]
			return "\n".join(formatted_vars)
		else:
			return "None"

	def get_shrinked_variables(self, name, value):
		""" There can be only 80 lines in a discord embed. Shrink value
			fit to that requirement. """
		str_value = str(value)

		if len(name) + len(" = ") + len(str_value) > 80:
			available_space = 80 - len(name) - len(" = ") - len(" ... ")
			len_a = available_space // 2
			len_b = available_space - len_a

			a = str_value[:len_a + 1]
			b = str_value[-1*len_b:]
			return f"{name} = {a} ... {b}"
		else:
			return f"{name} = {str_value}"

	@cmd.command()
	@checks.is_officer()
	async def mute(self, ctx):
		""" Set wether command executor will print every output/message to discord. """
		if self._mute is True:
			self._mute = False
		else:
			self._mute = True

		# Mute message will always be displayed to avoid confusion
		await ctx.send(f"Mute set to {self._mute}")

	@cmd.command()
	@checks.is_officer()
	async def flush(self, ctx):
		self._variables = dict()

		if self._mute is False:
			await ctx.send(f"Variables flushed.")

	@cmd.command()
	@checks.is_officer()
	async def execute(self, ctx, *, args):
		""" Execute a single lined statement """
		code_out = StringIO()
		old_out = sys.stdout
		sys.stdout = code_out
		before_locals = None
		before_locals = locals().copy()

		try:
			try:
				exec(args, {}, self._variables)
			except Exception as e:
				trace_back = traceback.format_exc()
				for c in chunks(trace_back, 1024):
					embed = discord.Embed(title="Command Executor", description=f"command : {args}")
					embed.add_field(name=f"Error : {str(e)}", value=c, inline=False)
					async with ctx.typing():
						await ctx.send(embed=embed)
			else:
				after_locals = locals().copy()
				new_variables = set(after_locals) - set(before_locals)
				difference_dict = {k: after_locals[k] for k in new_variables}
				self._variables.update(difference_dict)

				if self._mute is True:
					return

				code_out_str = code_out.getvalue()
				s = code_out_str if len(code_out_str) > 0 else "None"

				for c in chunks(s, 1024):
					embed = discord.Embed(title="Command Executor", description=f"command : {args}")
					embed.add_field(name=f"Output", value=c, inline=False)
					async with ctx.typing():
						await ctx.send(embed=embed)
			finally:
				sys.stdout = old_out
				code_out.close()
		except Exception as e:
			print(e)
			print(traceback.format_exc())


def setup(bot):
	bot.add_cog(CommandExecutor(bot))


if __name__ == "__main__":
	pass