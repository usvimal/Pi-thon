import asyncio
import platform
import subprocess
import config

from discord.ext import commands


class Brawlhalla(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def ping(self, host):
		"""
		Returns True if host (str) responds to a ping request.
		Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
		"""

		# Option for the number of packets as a function of
		param = '-n' if platform.system().lower() == 'windows' else '-c'

		# Building the command. Ex: "ping -c 1 google.com"
		command = ['ping', param, '1', host]

		return subprocess.run(command) == 0

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		try:
			if after.activity.name == 'Spotify' and before.id == config.creatorID:
				pong = self.ping('pingtest-sgp.brawlhalla.com')
				if pong:
					print('Brawl is up')
					channel = self.bot.get_user(after.id)
					await channel.send('Oof! Brawlhalla is down! I will let you know when its back up')

					async def check():
						while pong:
							self.ping('pingtest-sgp.brawlhalla.com')
							await asyncio.sleep(60 * 5)
						await channel.send('yay its back up!')

					await check()
				elif not pong:
					print('Brawl is down')

		except Exception as e:
			print(e)


def setup(bot):
	bot.add_cog(Brawlhalla(bot))
