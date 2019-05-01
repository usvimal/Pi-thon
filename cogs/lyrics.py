import discord
import cogs.utils.lyricsretriever
from discord.ext import commands


def chunks(s, n):
	"""Produce `n`-character chunks from `s`."""
	for start in range(0, len(s), n):
		yield s[start:start + n]


class Lyrics(commands.Cog):
	SPOTIFY = "Spotify"

	def __init__(self, bot):
		""" Create a lyrics retriever and add a list of registered user and their context"""
		self.bot = bot
		self.lyrics_retriever = cogs.utils.lyricsretriever.LyricsRetriever()
		self.user_context_dict = dict()

	@commands.group()
	async def lyrics(self, ctx):
		""" Show the lyrics of the song curretnly playing in Spotify"""
		if ctx.invoked_subcommand is None:
			await ctx.send('Oof owie, that was not a valid command 🤨')
		elif ctx.subcommand_passed is None:
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
		await ctx.send("Current lyric source is {}.".format(self.lyrics_retriever.get_main_source()))

	@lyrics.command()
	async def change_source(self, ctx, new_source):
		try:
			self.lyrics_retriever.change_main_source(new_source)
			await ctx.send("Changing of main source is successful.")
		except Exception as e:
			await ctx.send(str(e))

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
				await self.show_lyrics_from_description(ctx, *after_description)

	def get_song_description(self, user):
		""" Get the description of a song from user if the user is playing a song on Spotify. """
		if user.activities is not None:
			for activity in user.activities:
				if str(activity) == Lyrics.SPOTIFY:
					return activity.title, activity.artist
				else:
					raise Exception("You must be playing a Spotify song first.")

	async def show_lyrics_from_description(self, ctx, song_title, song_artist):
		"""Discord bot will show lyrics of a song from its description."""
		for chunk in chunks(self.lyrics_retriever.get_lyrics(song_title, song_artist), 2048):
			em = discord.Embed(title=song_title, description=chunk)
			em = em.set_author(name=song_artist)
			async with ctx.typing():
				await ctx.send(embed=em)

	@change_source.error
	async def change_source_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			return await ctx.send('Please add the source you want to get lyrics from. \n The sources available are: \n'
								  '1.genius \n2.lyrics-wiki')

	async def on_command_error(error):
		if isinstance(error, commands.CommandInvokeError):
			return print('Please play a song to get the lyrics 🙃')


def setup(bot):
	bot.add_cog(Lyrics(bot))

if __name__ == "__main__":
	a = discord.ext.commands.Bot("!")
	b = Lyrics(a)
	a.add_cog(b)
