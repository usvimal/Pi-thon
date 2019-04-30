import lyricsgenius
import os
import pylyrics3


class LyricsRetriever:
    GENIUS_TOKEN = "genius_token"
    GENIUS_SOURCE_NAME = "genius"
    WIKI_SOURCE_NAME = "lyrics-wiki"
    
    def __init__(self):
        self._sources = self._init_sources()
        self.main_source = list(self._sources.keys())[0]
        
    def _init_sources(self):
        """ Returns a dictionary with (key:value) pair with the key being the lyrics source name
            and the value being the function to retrieve lyrics """
        
        return_dict = dict()

        try:
            genius_api = lyricsgenius.Genius(os.environ.get(LyricsRetriever.GENIUS_TOKEN))
            return_dict[LyricsRetriever.GENIUS_SOURCE_NAME] = lambda title, artist: genius_api.search_song(title, artist).lyrics
        except:
            pass
        return_dict[LyricsRetriever.WIKI_SOURCE_NAME] = lambda title, artist: pylyrics3.get_song_lyrics(artist, title)

        return return_dict

    def get_main_source(self):
        """ Return the main source which is a string """
        return self.main_source

    def change_main_source(self, new_source):
        """ Change the main source with the given new source. If the new source is invalid, raise Exception """
        if new_source in self._sources:
            self.main_source = new_source
        else:
            raise Exception("Given source is not available in the list of sources.")
        
    def get_lyrics(self, title, artist):
        """ Get the lyrics from the source """
        lyrics = self._sources[self.main_source](title, artist)
        if lyrics is not None:
            return lyrics
        else:
            raise Exception("Unable to find lyrics in the main source.")
        
if __name__ == "__main__":
    retriever = LyricsRetriever()
    print(retriever.get_lyrics("Believer", "Imagine Dragons"))
    
