from discord.ext import commands
import discord
import os
import lyricsgenius
import asyncio


def chunks(s, n):
	"""Produce `n`-character chunks from `s`."""
	for start in range(0, len(s), n):
		yield s[start:start + n]


class Lyrics(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		genius_token = os.environ.get("genius_token")
		self.genius = lyricsgenius.Genius(genius_token)

	@commands.group()
	async def lyrics(self, ctx):
		if ctx.invoked_subcommand is None:
			song_title, song_artist = self.get_song_description(ctx.message.author.activity)
			await self.show_lyrics_from_description(song_title, song_artist)

	@lyrics.command()
	async def start(self, ctx):
		song_title, song_artist = self.get_song_description(ctx.message.author.activity)
		await self.show_lyrics_from_description(song_title, song_artist)

	async def on_member_update(self, before, after):
			if after.activity == "None":
				return None
			else:
					before_description = self.get_song_description(before.activity)
					after_description = self.get_song_description(after.activity)
					if before_description != after_description:
							await self.show_lyrics_from_description(*after_description)

	def get_song_description(self, activity):
		""" Get the description of a song from user activity. """
		return activity.title, activity.artist

	def get_lyrics(self, song_title, song_artist):
		""" Get lyrics from the song description. """
		return self.genius.search_song(song_title, song_artist).lyrics

	async def show_lyrics_from_description(self, song_title, song_artist):
		"""Discord bot will show lyrics of a song from its description."""
		for chunk in chunks(self.get_lyrics(song_title, song_artist), 2048):
			try:
				em = discord.Embed(title=song_title, description=chunk)
				em = em.set_author(name='Genius')
				async with self.bot.typing():
					await self.bot.send(embed=em)
			except AttributeError:
				await self.bot.send('Make sure you are playing a song on Spotify first!')


def setup(bot):
	bot.add_cog(Lyrics(bot))
