from discord.ext import commands
import discord
import os
import lyricsgenius


def chunks(s, n):
	"""Produce `n`-character chunks from `s`."""
	for start in range(0, len(s), n):
		yield s[start:start + n]


class Lyrics(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group()
	async def lyrics(self, ctx):
		song_title = ctx.message.author.activity.title
		song_artist = ctx.message.author.activity.artist
		genius_token = os.environ.get("genius_token")
		genius = lyricsgenius.Genius(genius_token)
		song = genius.search_song(song_title, song_artist)
		for chunk in chunks(song.lyrics, 2048):
			try:
				em = discord.Embed(title='L Y R I C S', description=chunk)
				em = em.set_author(name='Genius')
				async with ctx.typing():
					await ctx.send(embed=em)
			except AttributeError:
				await ctx.send('Make sure you are playing a song on Spotify first!')

	@lyrics.command()
	async def start(self, ctx):
		await self.lyrics()

	async def on_member_update(self, before, after):
		if before.activity.title != after.activity.title:
			await self.lyrics()
		if after.activity == 'None':
			return


def setup(bot):
	bot.add_cog(Lyrics(bot))
