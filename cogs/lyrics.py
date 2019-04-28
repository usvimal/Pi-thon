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
			await self.show_lyrics_from_description(ctx, song_title, song_artist)

	@lyrics.command()
	async def start(self, ctx):
<<<<<<< HEAD
<<<<<<< HEAD
		""" Register the user to the user-context dictionary and show the first song"""
		if ctx.author not in self.user_context_dict:
			self.user_context_dict[ctx.author] = ctx
			song_title, song_artist = self.get_song_description(ctx.message.author.activity)
			await self.show_lyrics_from_description(ctx, song_title, song_artist)
		else:
			ctx.send("You cannot use \";lyrics start\" again. Use \";lyrics change\" to change the context.")

	@lyrics.command()
	async def change(self, ctx):
		if ctx.author in self.user_context_dict:
			if self.user_context_dict[ctx.author] == ctx:
				ctx.send("Current context is the original context for you.")
			else:
				self.user_context_dict[ctx.author] = ctx
				ctx.send("Context changed for you.")
		else:
			ctx.send("Use \";lyrics start\" to register first.")

	@lyrics.command()
	async def stop(self, ctx):
		""" Deregister the user from the dictionary """
		if ctx.author in self.user_context_dict:
			del self.user_context_dict[ctx.author]
		else:
			ctx.send("You must use \";lyrics start\" first before using this command.")
=======
		song_title, song_artist = self.get_song_description(ctx.message.author.activity)
		await self.show_lyrics_from_description(ctx, song_title, song_artist)
>>>>>>> parent of ec3ad14... 2nd update to lyrics.py by Min

	async def on_member_update(self, before, after):
<<<<<<< HEAD
		""" If the user is registered and the next activity is still Spotify, show new lyrics. """
		if before in self.user_context_dict and after.activity == discord.Spotify:
			# Get the context of registered user and update the dictionary
			ctx = self.user_context_dict[before]
			del self.user_context_dict[before]
			self.user_context_dict[after] = ctx

			before_description = self.get_song_description(before.activity)
			after_description = self.get_song_description(after.activity)
			if before_description != after_description:
				await self.show_lyrics_from_description(ctx, *after_description)
=======
=======
		song_title, song_artist = self.get_song_description(ctx.message.author.activity)
		await self.show_lyrics_from_description(ctx, song_title, song_artist)

	async def on_member_update(self, before, after):
>>>>>>> parent of ec3ad14... 2nd update to lyrics.py by Min
			if after.activity == "None":
				return None
			else:
					before_description = self.get_song_description(before.activity)
					after_description = self.get_song_description(after.activity)
					if before_description != after_description:
							await self.show_lyrics_from_description(*after_description)
<<<<<<< HEAD
>>>>>>> parent of ec3ad14... 2nd update to lyrics.py by Min
=======
>>>>>>> parent of ec3ad14... 2nd update to lyrics.py by Min

	def get_song_description(self, activity):
		""" Get the description of a song from user activity. """
		if activity == discord.Spotify:
			return activity.title, activity.artist
		else:
			raise Exception("You must be playing a song from Spotify.")

	def get_lyrics(self, song_title, song_artist):
		""" Get lyrics from the song description. """
		return self.genius.search_song(song_title, song_artist).lyrics

	async def show_lyrics_from_description(self, ctx, song_title, song_artist):
		"""Discord bot will show lyrics of a song from its description."""
		try:
			for chunk in chunks(self.get_lyrics(song_title, song_artist), 2048):
				em = discord.Embed(title=song_title, description=chunk)
				em = em.set_author(name='Genius')
				async with ctx.typing():
					await ctx.send(embed=em)
		except Exception as e:
			await ctx.send(str(e))



def setup(bot):
	bot.add_cog(Lyrics(bot))
