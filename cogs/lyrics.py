import asyncio
import discord
import lyricsgenius
import os
import pylyrics3
from discord.ext import commands


def chunks(s, n):
	"""Produce `n`-character chunks from `s`."""
	for start in range(0, len(s), n):
		yield s[start:start + n]


class Lyrics(commands.Cog):
	def __init__(self, bot):
		""" Registers genius token and add a list of registered user and their context"""
		self.bot = bot
		self.source = "Genius"
		self.genius = lyricsgenius.Genius(os.environ.get("genius_token"))
		self.user_context_dict = dict()

	@commands.group()
	async def lyrics(self, ctx):
		if ctx.invoked_subcommand is None:
			song_title, song_artist = self.get_song_description(ctx.author)
			await self.show_lyrics_from_description(ctx, song_title, song_artist)

	@lyrics.command()
	async def start(self, ctx):
		""" Register the user to the user-context dictionary and show the first song"""
		if ctx.author not in self.user_context_dict:
			self.user_context_dict[ctx.author] = ctx
			song_title, song_artist = self.get_song_description(ctx.author)
			await self.show_lyrics_from_description(ctx, song_title, song_artist)
		else:
			await ctx.send("\";lyrics start\" has already been activated.")

	@lyrics.command()
	async def stop(self, ctx):
		""" Deregister the user from the dictionary """
		if ctx.author in self.user_context_dict:
			del self.user_context_dict[ctx.author]
			await ctx.send("You will stop receiving lyrics now.")
		else:
			await ctx.send("You are not registered to receive lyrics. Use \";lyrics start\" to start receiving lyrics.")

	@lyrics.command()
	async def source(self, ctx):
		await ctx.send("Current lyric source is {}.".format(self.source))

	@lyrics.command()
	async def change_source(self, ctx):
		if self.source == "Genius":
			self.source = "Lyrics-Wikia"
		elif self.source == "Lyrics-Wikia":
			self.source = "Genius"
		await ctx.send("Changed lyric source to {}".format(self.source))

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		""" If the user is registered and the next activity is still Spotify, show new lyrics. """
		if before in self.user_context_dict and after.activity != "None":
				# Get the context of registered user and update the dictionary
				ctx = self.user_context_dict[before]
				del self.user_context_dict[before]
				self.user_context_dict[after] = ctx

				before_description = self.get_song_description(before)
				after_description = self.get_song_description(after)
				if before_description != after_description:
						await self.show_lyrics_from_description(ctx, *after_description)

	def get_song_description(self, user):
		""" Get the description of a song from user if the user is playing a song on Spotify. """
		if user.activity == discord.Spotify:
			return user.activity.title, user.activity.artist
		else:
			# TODO: Error Catching
			pass

	def get_lyrics(self, song_title, song_artist):
		if self.source == "Genius":
			return self.get_lyrics_genius(song_title, song_artist)
		elif self.source == "Lyrics-Wikia":
			return self.get_lyrics_genius(song_title, song_artist)
		return None

	def get_lyrics_genius(self, song_title, song_artist):
		""" Get lyrics from the song description using the Genius API. """
		return self.genius.search_song(song_title, song_artist).lyrics

	def get_lyrics_wiki(self, song_title, song_artist):
		return pylyrics3.get_song_lyrics(song_artist, song_title)

	async def show_lyrics_from_description(self, ctx, song_title, song_artist):
		"""Discord bot will show lyrics of a song from its description."""
		for chunk in chunks(self.get_lyrics(song_title, song_artist), 2048):
			em = discord.Embed(title=song_title, description=chunk)
			em = em.set_author(name=song_artist)
			async with ctx.typing():
				await ctx.send(embed=em)

def setup(bot):
	bot.add_cog(Lyrics(bot))
