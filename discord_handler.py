import discord
import logging
import asyncio


class DiscordHandler(logging.Handler):
	def __init__(self, channel):
		super().__init__()
		self._channel = channel

	def emit(self, record):
		loop = asyncio.get_running_loop()
		print("emitted")
		loop.run_until_complete(self.send_to_channel(self.format(record)))

	async def send_to_channel(self, msg):
		print("send_to_channel started")
		for part in self._chunk(msg, 1999):
			async with self._channel.typing():
				await self._channel.send(msg)

	@staticmethod
	def _chunk(target_str, chunk_size):
		for i in range(0, len(target_str), chunk_size):
			yield target_str[i: i+chunk_size]
