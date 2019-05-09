import lyricsgenius
import os
import pylyrics3
from discord.ext import commands


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
		""" Create sources and return as a Sourc Name: Source Object pair. """
		return_dict = dict()

		return_dict[LyricsRetriever.GENIUS_SOURCE_NAME] = LyricsRetriever.genius_get_lyrics
		return_dict[LyricsRetriever.WIKI_SOURCE_NAME] = LyricsRetriever.lyrics_wiki_get_lyrics

		return return_dict

	@staticmethod
	def estimate_song_words(lyrics):
		""" This is an attempt to weed out false positives in song search. """
		return len(lyrics.split())

	def __init__(self):
		self._sources = self._create_sources()
		self.main_source = list(self._sources.keys())[0]

	def get_main_source(self):
		return self.main_source

	def change_main_source(self, new_source):
		if new_source in self._sources:
			self.main_source = new_source
		else:
			raise self.SourceChangeNotSuccess

	def get_lyrics(self, title, artist):
		# Retrieve source object from the _sources dictionary and  attempt to get the lyrics.
		lyrics = self._sources[self.main_source](title, artist)
		if lyrics is not None and self.estimate_song_words(lyrics) <= self.AVERAGE_SONG_WORD_SIZE:
			return lyrics
		else:
			raise self.LyricsNotFoundException


if __name__ == "__main__":
	pass
