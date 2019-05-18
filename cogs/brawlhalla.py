import asyncio
import platform
import subprocess

from discord.ext import commands


class Brawlhalla(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.up = ''

	def ping(self, host):
		"""
		Returns True if host (str) responds to a ping request.
		Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
		"""

		# Option for the number of packets as a function of
		param = '-n' if platform.system().lower() == 'windows' else '-c'

		# Building the command. Ex: "ping -c 1 google.com"
		command = ['ping', param, '1', host]

		if subprocess.call(command) == 0:
			self.up = True
		else:
			self.up = False

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		try:
			if after.activity.name == 'Brawlhalla' and self.bot.brawlhalla_status.get(before.id, default=False) is True:
				self.ping('pingtest-sgp.brawlhalla.com')
				if not self.up:
					channel = self.bot.get_user(after.id)
					await channel.send('Oof! Brawlhalla is down! I will let you know when its back up')

					async def check():
						while not self.up:
							self.ping('pingtest-sgp.brawlhalla.com')
							await asyncio.sleep(60 * 5)
						await channel.send('yay Brawlhalla is back up! Go play :)')

					await check()
		except:
			pass


def setup(bot):
	bot.add_cog(Brawlhalla(bot))
