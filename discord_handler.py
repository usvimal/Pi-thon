import discord
import logging
import asyncio

""" Handler which is used to make loggers print to discord.	"""
class DiscordHandler(logging.Handler):
	def __init__(self, channel, main_loop, level=logging.NOTSET):
		super().__init__(level)
		self._channel = channel
		self._main_loop = main_loop

		self._set_formatter()

	def _set_formatter(self):
		str_format = """Logging Level : %(levelname)s\n
						Logger        : %(name)s\n
						Time created  : %(asctime)s\n
						Source Path   : %(pathname)s\n
						Function Name : %(funcName)s\n
						Message       : %(message)s"""
		self.setFormatter(logging.Formatter(str_format))

	def emit(self, record):
		self._main_loop.run_until_complete(self.send_to_channel(self.format(record)))

	async def send_to_channel(self, msg):
		async with self._channel.typing():
			await self._channel.send(msg)