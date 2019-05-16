import discord

from discord.ext import commands
from utils.text_formatter import chunks
from utils.lyricsretriever import LyricsRetriever


class Lyrics(commands.Cog):
	class SpotifyNotPlaying(commands.CommandError):
		pass

	SPOTIFY = "Spotify"

	def __init__(self, bot):
		""" Create a lyrics retriever and add a list of registered user and their context"""
		self.bot = bot
		self.lyrics_retriever = LyricsRetriever()
		self.user_context_dict = dict()

	@commands.group()
	async def lyrics(self, ctx):
		""" Show the lyrics of the song curretnly playing in Spotify"""
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed:
				await ctx.send('Oof owie, that was not a valid command 🤨')
			else:
				song_title, song_artist = self.get_song_description(ctx.author)
				await self.show_lyrics_from_description(ctx, song_title, song_artist)

	@lyrics.command(aliases=["begin"])
	async def start(self, ctx):
		""" Register the user to the user-context dictionary and show the first song"""
		if ctx.author not in self.user_context_dict:
			song_title, song_artist = self.get_song_description(ctx.author)
			await self.show_lyrics_from_description(ctx, song_title, song_artist)
			self.user_context_dict[ctx.author] = ctx
		else:
			await ctx.send("\";lyrics start\" has already been activated.")

	@lyrics.command(aliases=["end"])
	async def stop(self, ctx):
		""" Deregister the user from the dictionary """
		if ctx.author in self.user_context_dict:
			del self.user_context_dict[ctx.author]
			await ctx.send("You will stop receiving lyrics now.")
		else:
			await ctx.send("You are not registered to receive lyrics. Use \";lyrics start\" to start receiving lyrics.")

	@lyrics.command()
	async def source(self, ctx):
		await ctx.send("Current lyric source is {}.".format(self.lyrics_retriever.get_main_source()))

	@lyrics.command()
	async def change_source(self, ctx, new_source):
		self.lyrics_retriever.change_main_source(new_source)
		await ctx.send("Changing of main source is successful.")

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		""" If the user is registered and the next activity is still Spotify, show new lyrics. """
		if before in self.user_context_dict and str(after.activity) == Lyrics.SPOTIFY:
			# Get the context of registered user and update the dictionary
			ctx = self.user_context_dict[before]
			del self.user_context_dict[before]
			self.user_context_dict[after] = ctx
			before_description = self.get_song_description(before)
			after_description = self.get_song_description(after)
			if before_description != after_description:
				try:
					await self.show_lyrics_from_description(ctx, *after_description)
				except LyricsRetriever.LyricsNotFoundException:
					await ctx.send("Current lyrics source {} could not retrieve the lyrics.".format(self.lyrics_retriever.get_main_source()))

	def get_song_description(self, user):
		""" Get the description of a song from user if the user is playing a song on Spotify. """
		if user.activities is not None:
			for activity in user.activities:
				if str(activity) == Lyrics.SPOTIFY:
					return activity.title, activity.artist
		raise self.SpotifyNotPlaying

	async def show_lyrics_from_description(self, ctx, song_title, song_artist):
		"""Discord bot will show lyrics of a song from its description."""
		for chunk in chunks(self.lyrics_retriever.get_lyrics(song_title, song_artist), 2048):
			em = discord.Embed(title=song_title, description=chunk)
			em = em.set_author(name=song_artist)
			async with ctx.typing():
				await ctx.send(embed=em)

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		""" Error thrown by commands will be of the type discord.ext.command.CommandError. For errors not inheriting
		from CommandError, it will be difficult to error handle. """
		if isinstance(error, self.SpotifyNotPlaying):
			await ctx.send("Please play a song to get the lyrics 🙃")
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Invalid usage of command. Use ;help lyrics for more information.")
		elif hasattr(error, "original") and isinstance(error.original, LyricsRetriever.LyricsNotFoundException):
			await ctx.send("Current lyrics source {} could not retrieve the lyrics.".format(
				self.lyrics_retriever.get_main_source()))
		elif hasattr(error, "original") and isinstance(error.original, LyricsRetriever.SourceChangeNotSuccess):
			await ctx.send("Invalid argument for song sources.\nValid arguments are:\n\t1. genius \n\t2. lyrics-wiki")


def setup(bot):
	bot.add_cog(Lyrics(bot))


if __name__ == "__main__":
	pass
