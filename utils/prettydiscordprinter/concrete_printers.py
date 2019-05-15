from utils.prettydiscordprinter.abstract_classes import PrettyAbstractPrinter
from utils.prettydiscordprinter.concrete_formatters import *


class PrettyTextPrinter(PrettyAbstractPrinter):
	""" Normal text printing to discord """
	def __init__(self):
		super().__init__()

		self._chr_limit = 2000
		self._chr_per_line = 100

	def _configure_formatter(self, formatter):
		if isinstance(formatter, LinePrefixFormatter):
			formatter.configure(self._chr_per_line)
		return formatter
