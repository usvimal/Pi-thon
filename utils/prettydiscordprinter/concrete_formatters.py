from utils.chunker import chunks
from utils.prettydiscordprinter.abstract_classes import PrettyAbstractFormatter


class LinePrefixFormatter(PrettyAbstractFormatter):
	""" Add given prefix before the line. Will override the default discord characters per line
		depending on the printer. Can be used to emulate the looks of a console and etc ... """
	def __init__(self, line_prefix):
		self._line_prefix = line_prefix
		self._chr_per_line = None

	def configure(self, chr_per_line):
		self._chr_per_line = chr_per_line

	def pretty_format(self, text):
		return_text = ""
		for line in text.split("\n"):
			for sub_line in chunks(text, self._chr_per_line - len(self._line_prefix)):
				return_text += self._line_prefix + sub_line + "\n"

		return return_text