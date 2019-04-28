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
		""" Registers genius token and add a list of registered user and their context"""
		self.bot = bot
		genius_token = os.environ.get("genius_token")
		self.genius = lyricsgenius.Genius(genius_token)
		self.user_context_dict = dict()

	@commands.group()
	async def lyrics(self, ctx):
		if ctx.invoked_subcommand is None:
			song_title, song_artist = self.get_song_description(ctx.message.author.activity)
			await self.show_lyrics_from_description(ctx, song_title, song_artist)

	@lyrics.command()
	async def start(self, ctx):
		""" Register the user to the user-context dictionary and show the first song"""
		if ctx.author not in self.user_context_dict:
			self.user_context_dict[ctx.author] = ctx
			song_title, song_artist = self.get_song_description(ctx.message.author.activity)
			await self.show_lyrics_from_description(ctx, song_title, song_artist)

	@lyrics.command()
	async def stop(self, ctx):
		""" Deregister the user from the dictionary """
		if ctx.author in self.user_context_dict:
			del self.user_context_dict[ctx.author]

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		""" If the user is registered and the next activity is still Spotify, show new lyrics. """
		if before in self.user_context_dict and after.activity != "None":
				# Get the context of registered user and update the dictionary
				ctx = self.user_context_dict[before]
				del self.user_context_dict[before]
				self.user_context_dict[after] = ctx

				before_description = self.get_song_description(ctx, before.activity)
				after_description = self.get_song_description(ctx, after.activity)
				if before_description != after_description:
						await self.show_lyrics_from_description(ctx, *after_description)


	def get_song_description(self, ctx, activity):
		""" Get the description of a song from user activity. """
		try:
			return activity.title, activity.artist
		except AttributeError:
			await ctx.send('Make sure you are playing a song on Spotify first!')


	def get_lyrics(self, ctx, song_title, song_artist):
		""" Get lyrics from the song description. """
		try:
			return self.genius.search_song(song_title, song_artist).lyrics
		except AttributeError:
			await ctx.send('Make sure you are playing a song on Spotify first!')

	async def show_lyrics_from_description(self, ctx, song_title, song_artist):
		"""Discord bot will show lyrics of a song from its description."""
		for chunk in chunks(self.get_lyrics(ctx, song_title, song_artist), 2048):
			em = discord.Embed(title=song_title, description=chunk)
			em = em.set_author(name=song_artist)
			async with ctx.typing():
				await ctx.send(embed=em)


def setup(bot):
	bot.add_cog(Lyrics(bot))
