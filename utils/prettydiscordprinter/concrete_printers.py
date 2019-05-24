import asyncio

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


class DelayedPrinterWrapper(PrettyTextPrinter):
	""" Wraps the printer to wait a specified amount of time before printing. If a new message is requested during this
		waiting time, it will be appended to the current message and the timer will reset. When the timer is up, begin
		printing. """
	SLEEP_DURATION = 0.5

	def __init__(self, printer, delay=5.0):
		self._printer = printer
		self._delay = delay
		self._queue = None
		self._text = None

	def add_formatters(self, *formatters):
		self._printer.add_formatters(*formatters)

	def add_formatter(self, formatter):
		self._printer.add_formatter(formatter)

	async def pretty_print(self, ctx, text):
		if self._queue is None:
			self._queue = []
			self._text = []
			asyncio.get_event_loop().create_task(self.check_message_updates(ctx))
		self._queue.append(text)

	async def check_message_updates(self, ctx):
		i = 0
		max_i = int(self._delay / DelayedPrinterWrapper.SLEEP_DURATION) + 1

		while i < max_i:
			i += 1
			await asyncio.sleep(DelayedPrinterWrapper.SLEEP_DURATION)
			if len(self._queue) > 0:
				self._text.extend(self._queue)
				self._queue.clear()
				i = 0

		await self._printer.pretty_print(ctx, "\n".join(self._text))
		self._queue = None
		self._text = None


