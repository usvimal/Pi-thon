import lyricsgenius
import os
import pylyrics3


class LyricsRetriever:
	class LyricsNotFoundException(Exception):
		pass

	class SourceChangeNotSuccess(Exception):
		pass

	GENIUS_TOKEN = "genius_token"
	GENIUS_SOURCE_NAME = "genius"
	WIKI_SOURCE_NAME = "lyrics-wiki"
	AVERAGE_SONG_WORD_SIZE = 1000		# Estimated and added 200 words more, for benefit of doubt

	@staticmethod
	def genius_get_lyrics(title, artist):
		genius_api = lyricsgenius.Genius(os.environ.get(LyricsRetriever.GENIUS_TOKEN))
		song = genius_api.search_song(title, artist)
		if song is not None:
			return song.lyrics
		else:
			return None

	@staticmethod
	def lyrics_wiki_get_lyrics(title, artist):
		return pylyrics3.get_song_lyrics(artist, title)

	@staticmethod
	def _create_sources():
		""" Create sources and return as a Source Name: Source Object pair. """
		return_dict = dict()

		return_dict[LyricsRetriever.GENIUS_SOURCE_NAME] = LyricsRetriever.genius_get_lyrics
		return_dict[LyricsRetriever.WIKI_SOURCE_NAME] = LyricsRetriever.lyrics_wiki_get_lyrics

		return return_dict

	@staticmethod
	def estimate_song_words(lyrics):
		""" This is an attempt to weed out false positives in song search. """
		return len(lyrics.split())

	def __init__(self, bot):
		self.bot = bot
		self._sources = self._create_sources()

	def get_main_source(self, user_id):
		return self.bot.lyrics_source.get(user_id)

	async def change_main_source(self, user_id, new_source):
		if user_id in self.bot.lyrics_source:
			async with self.bot.dbpool.acquire() as conn:
				await conn.execute('UPDATE userprop SET "lyrics_source"=$1 WHERE "user_id"=$2;',
				                   new_source, user_id)
		else:
			async with self.bot.dbpool.acquire() as conn:
				await conn.execute('INSERT INTO userprop ("user_id", "lyrics_source") VALUES ($1, $2);',
				                   user_id, new_source)
		self.bot.lyrics_source[user_id] = new_source

	def get_lyrics(self, user_id, title, artist):
		# Retrieve source object from the _sources dictionary and  attempt to get the lyrics.
		lyrics = self._sources[self.get_main_source(user_id)](title, artist)
		if lyrics is not None and self.estimate_song_words(lyrics) <= self.AVERAGE_SONG_WORD_SIZE:
			return lyrics
		else:
			raise self.LyricsNotFoundException


if __name__ == "__main__":
	pass
