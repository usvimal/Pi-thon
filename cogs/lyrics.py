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
		self.lyrics_retriever = LyricsRetriever(bot)
		self.user_context_dict = dict()

	@commands.group()
	async def lyrics(self, ctx):
		""" Show the lyrics of the song currently playing in Spotify"""
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed:
				em = discord.Embed(title='Oof! That was not a valid command 🤨 ',
				                   description='Type ;help [command] for more info on a command.',
				                   colour=0x3c1835)
				await ctx.send(embed=em, delete_after=60)
			else:
				song_title, song_artist = self.get_song_description(ctx.author)
				await self.show_lyrics_from_description(ctx, song_title, song_artist)

	@lyrics.command(aliases=["begin"])
	async def start(self, ctx):
		""" Show lyrics for all the songs the user plays until they stop this"""
		if ctx.author not in self.user_context_dict:
			song_title, song_artist = self.get_song_description(ctx.author)
			await self.show_lyrics_from_description(ctx, song_title, song_artist)
			self.user_context_dict[ctx.author] = ctx
		else:
			await ctx.send("\";lyrics start\" has already been activated.")

	@lyrics.command(aliases=["end"])
	async def stop(self, ctx):
		""" Stop showing new lyrics """
		if ctx.author in self.user_context_dict:
			del self.user_context_dict[ctx.author]
			await ctx.send("You will stop receiving lyrics now.")
		else:
			await ctx.send("You are not registered to receive lyrics. Use \";lyrics start\" to start receiving lyrics.")

	@lyrics.command()
	async def source(self, ctx):
		""" Show the current source for lyrics"""
		current_source = self.lyrics_retriever.get_main_source(ctx.author.id)
		await ctx.send(f"Current lyric source is {current_source}.")

	@lyrics.command()
	async def change_source(self, ctx):
		""" Change the lyrics source"""
		em = discord.Embed(title='Choose your source:', description='\t1. genius \n\t2. lyrics-wiki', color=0xbd6c24)
		em.set_footer(text="Send the number corresponding to the lyrics source")
		await ctx.send(embed=em)
		check = lambda m: m.author == ctx.author and m.channel == ctx.channel
		msg = await self.bot.wait_for("message", timeout=10, check=check)
		new_source = ''
		if int(msg.content) == 1:
			new_source = 'genius'
		elif int(msg.content) == 2:
			new_source = 'lyrics-wiki'
		await self.lyrics_retriever.change_main_source(ctx.author.id, new_source)
		await ctx.send(f"Changing of lyrics source to `{new_source}` is successful.")

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
					await ctx.send(f"Current lyrics source {self.lyrics_retriever.get_main_source(after.id)} could not retrieve the lyrics.")

	def get_song_description(self, user):
		""" Get the description of a song from user if the user is playing a song on Spotify. """
		if user.activities is not None:
			for activity in user.activities:
				if str(activity) == Lyrics.SPOTIFY:
					return activity.title, activity.artist
		raise self.SpotifyNotPlaying

	async def show_lyrics_from_description(self, ctx, song_title, song_artist):
		"""Discord bot will show lyrics of a song from its description."""
		for chunk in chunks(self.lyrics_retriever.get_lyrics(ctx.author.id, song_title, song_artist), 2048):
			em = discord.Embed(title=song_title, description=chunk)
			em = em.set_author(name=song_artist)
			await ctx.trigger_typing()
			await ctx.send(embed=em, delete_after=5*60)

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		""" Error thrown by commands will be of the type discord.ext.command.CommandError. For errors not inheriting
		from CommandError, it will be difficult to error handle. """
		if isinstance(error, self.SpotifyNotPlaying):
			await ctx.send("Please play a song to get the lyrics 🙃")
		elif hasattr(error, "original") and isinstance(error.original, LyricsRetriever.LyricsNotFoundException):
			await ctx.send("Current lyrics source {} could not retrieve the lyrics.".format(
				self.lyrics_retriever.get_main_source(ctx.author.id)))


def setup(bot):
	bot.add_cog(Lyrics(bot))


if __name__ == "__main__":
	pass
