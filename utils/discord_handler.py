import discord
import logging
import traceback

from utils.prettydiscordprinter import *


""" Handler which is used to make loggers print to discord.	"""
class DiscordHandler(logging.Handler):
	def __init__(self, channel, main_loop, level=logging.NOTSET):
		super().__init__(level)
		self._channel = channel
		self._main_loop = main_loop

		self._set_formatter()

	def _set_formatter(self):
		str_format = ("Logging Level: %(levelname)s\n"
						"Logger: %(name)s\n"
						"Time created: %(asctime)s\n"
						"Source Path: %(pathname)s\n"
						"Function Name: %(funcName)s\n"
						"Message: %(message)s\n")
		self.setFormatter(logging.Formatter(str_format))

	def emit(self, record):
		self._main_loop.create_task(self.send_to_channel(self.format(record)))

	async def send_to_channel(self, msg):
		async with self._channel.typing():
			em = discord.Embed(title='logger', description=msg, colour=0x19a934)
			await self._channel.send(embed=em)


class DiscordStdErr:
	def __init__(self, original_stderr, channel, main_loop):
		self._original_stderr = original_stderr
		self._channel = channel
		self._main_loop = main_loop

	# Override stderr write
	def write(self, text):
		if len(text) != 0:
			self._original_stderr.write(text)
			self._main_loop.create_task(self._send_to_channel(">>> " + text))

	async def _send_to_channel(self, msg):
		try:
			printer = PrettyTextPrinter()
			await printer.pretty_print(self._channel, msg)
		except Exception as e:
			self._original_stderr.write(str(e))
			self._original_stderr.write(traceback.format_exc())

