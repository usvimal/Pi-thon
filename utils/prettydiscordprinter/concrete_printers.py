import asyncio

from copy import deepcopy
from discord import Embed
from discord.ext.commands import Paginator
from utils.text_formatter import chunks
from utils.prettydiscordprinter.abstract_classes import PrettyAbstractPrinter
from utils.prettydiscordprinter.concrete_formatters import *


class PrettyTextPrinter(PrettyAbstractPrinter):
	""" Normal text printing to discord """
	def __init__(self):
		super().__init__()

		self._chr_limit = 2000

	def _configure_formatter(self, formatter):
		return formatter

	async def pretty_print(self, ctx, text):
		prettified_text = self._use_formatters(text)

		for chunk in chunks(prettified_text, self._chr_limit):
			async with ctx.typing():
				await ctx.send(chunk)


class PrettyCodeBlockPrinter(PrettyAbstractPrinter):
	""" Code block printing to discord """
	def __init__(self):
		super().__init__()

		self._chr_limit = 2000 - 6

	def _configure_formatter(self, formatter):
		return formatter

	async def pretty_print(self, ctx, text):
		prettified_text = self._use_formatters(text)

		for chunk in chunks(prettified_text, self._chr_limit):
			async with ctx.typing():
				await ctx.send(f"```{chunk}```")


class PrettyEmbedPrinter(PrettyAbstractPrinter):
	""" Embed printing to discord. Will be printed in description, not field. """
	def __init__(self, embed):
		super().__init__()

		self._chr_limit = 2048
		self._embed = embed

	def _configure_formatter(self, formatter):
		return formatter

	async def pretty_print(self, ctx, text):
		prettified_text = self._use_formatters(text)

		for chunk in chunks(prettified_text, self._chr_limit):
			embed_clone = deepcopy(self._embed)
			embed_clone.description = chunk
			async with ctx.typing():
				await ctx.send(embed=embed_clone)


class PrettyPaginator(PrettyAbstractPrinter):
	"""
	Shows a discord message with pages and reactions acting as the button. Users can move left, right, go to the first
	page, go to the last page, and delete the message by interacting with the buttons.
	Usage: PrettyPaginator().pretty_print(embeds) where embeds will act as the pages.
	"""
	def __init__(self):
		super().__init__()

		self._chr_limit = 2048

		self._entries = None
		self._reaction_emojis = [
			('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', self._first_page),
			('\N{BLACK LEFT-POINTING TRIANGLE}', self._previous_page),
			('\N{BLACK RIGHT-POINTING TRIANGLE}', self._next_page),
			('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', self._last_page),
			('\N{BLACK SQUARE FOR STOP}', self._stop_pages),
		]
		self._ctx = None
		self._message = None
		self._current_index = -1
		self._paginating = False
		self._match = None

	async def _first_page(self):
		await self._show_page(0)

	async def _previous_page(self):
		await self._show_page(self._current_index - 1)

	async def _next_page(self):
		await self._show_page(self._current_index + 1)

	async def _last_page(self):
		await self._show_page(len(self._entries) - 1)

	async def _show_page(self, index):
		# Do nothing if the index is out of range or index is the same as the current index
		if index not in range(0, len(self._entries)) or index == self._current_index:
			return

		self._current_index = index

		# Create new message if it is not created and then add reactions
		if self._message is None:
			self._message = await self._ctx.send(embed=self._entries[self._current_index])
			for (reaction, _) in self._reaction_emojis:
				await self._message.add_reaction(reaction)
		# If a message with reactions already exist, edit it
		else:
			await self._message.edit(embed=self._entries[self._current_index])

	async def _stop_pages(self):
		self._paginating = False

	def _react_check(self, reaction, user):
		if user is None or user.id != self._ctx.author.id:
			return False

		if reaction.message.id != self._message.id:
			return False

		for (emoji, func) in self._reaction_emojis:
			if reaction.emoji == emoji:
				self._match = func
				return True
		return False

	def _configure_formatter(self, formatter):
		return formatter

	async def pretty_print(self, ctx, entries):
		if self._entries is not None:
			raise Exception("Printer is being used for an exisiting scrollable embed. Create another printer or wait for"
							"the exisiting embed to expire after the given time")

		# Adds page numbers to the title
		for i, e in enumerate(entries, start=1):
			e.title += f"| Page {i} out of {len(entries)}"

		self._entries = entries
		self._ctx = ctx

		await self._show_page(0)
		self._paginating = True

		while self._paginating:
			try:
				reaction, user = await self._ctx.bot.wait_for('reaction_add', check=self._react_check, timeout=120.0)
			except asyncio.TimeoutError:
				self._paginating = False

			try:
				await self._message.remove_reaction(reaction, user)
			except:
				pass  # can't remove it so don't bother doing so

			await self._match()

		try:
			await self._message.delete()
		except:
			pass
		finally:
			self._ctx = None
			self._message = None
			self._current_index = -1
			self._match = None

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
			asyncio.get_event_loop().create_task(self._check_message_updates(ctx))
		self._queue.append(text)

	async def _check_message_updates(self, ctx):
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


