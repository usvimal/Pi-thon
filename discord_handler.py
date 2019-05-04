import discord
import logging
import asyncio


class DiscordHandler(logging.Handler):
	def __init__(self, channel):
		self._channel = channel

	def emit(self, record):
		print("emitted")
		self.send_to_channel(self.format(record))

	async def send_to_channel(self, msg):
		print("send_to_channel started")
		for part in self._chunk(msg, 1999):
			async with self._channel.typing():
				self._channel.send(msg)

	@staticmethod
	def _chunk(target_str, chunk_size):
		for i in range(0, len(target_str), chunk_size):
			yield target_str[i: i+chunk_size]
