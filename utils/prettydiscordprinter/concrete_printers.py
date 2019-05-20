from utils.prettydiscordprinter.abstract_classes import PrettyAbstractPrinter
from utils.prettydiscordprinter.concrete_formatters import *


class PrettyTextPrinter(PrettyAbstractPrinter):
	""" Normal text printing to discord """
	def __init__(self):
		super().__init__()

		self._chr_limit = 2000
		self._chr_per_line = 100

	def _configure_formatter(self, formatter):
		if isinstance(formatter, LinePrefixFormatter):
			formatter.configure(self._chr_per_line)
		return formatter


class PrettyCodeBlockPrinter(PrettyTextPrinter):
	""" Code block printing to discord """
	def __init__(self):
		super().__init__()

		self._chr_limit = 2000 - 6
		self._chr_per_line = 100

	def _configure_formatter(self, formatter):
		if isinstance(formatter, LinePrefixFormatter):
			formatter.configure(self._chr_per_line)
		return formatter

	async def pretty_print(self, ctx, text):
		prettified_text = self._use_formatters(text)

		for chunk in chunks(prettified_text, self._chr_limit):
			async with ctx.typing():
				await ctx.send(f"```{chunk}```")