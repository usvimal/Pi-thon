from discord.ext import commands
import discord
import os
import lyricsgenius
import asyncio


class Lyrics(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bg_task = self.loop.create_task(self.start())

	@commands.group()
	async def lyrics(self, ctx):
		song_title = ctx.message.author.activity.title
		song_artist = ctx.message.author.activity.artist
		genius_token = os.environ.get("genius_token")
		genius = lyricsgenius.Genius(genius_token)
		song = genius.search_song(song_title, song_artist)

		try:
			em = discord.Embed(title='lyrics', description=song.lyrics)
			em = em.set_author(name='Genius')
			async with ctx.typing():
				await ctx.send(embed=em)
		except ConnectionError:
			await ctx.send(song_title)
			await ctx.send(song.lyrics)
			return
		except AttributeError:
			await ctx.send('Make sure you are playing a song on Spotify first!')
		return

	@lyrics.command()
	async def start(self, ctx):
		await self.lyrics()

	async def on_member_update(self, before, after):
		if before.activity.title != after.activity.title:
			await self.lyrics
		if after.activity == 'None':
			return

