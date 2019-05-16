from utils.chunker import chunks

class PrettyAbstractPrinter:
	def __init__(self):
		self._formatters = []
		self._chr_limit = None				# Implement later
		self._chr_per_line = None			# Implement later

	def add_formatters(self, *formatters):
		for formatter in formatters:
			self.add_formatter(formatter)

	def add_formatter(self, formatter):
		self._formatters.append(self._configure_formatter(formatter))

	def _configure_formatter(self, formatter):
		""" Every formatter must be configured to fit the printer type. """
		raise NotImplementedError("Implement this abstract function later.")

	async def pretty_print(self, ctx, text):
		prettified_text = self._use_formatters(text)

		for chunk in chunks(prettified_text, self._chr_limit):
			async with ctx.typing():
				await ctx.send(chunk)

	def _use_formatters(self, text):
		copied_text = text
		for formatter in self._formatters:
			copied_text = formatter.pretty_format(copied_text)

		return copied_text



class PrettyAbstractFormatter:
	def __init__(self):
		raise NotImplementedError("Implement this abstract function later.")

	def configure(self, **kwargs):
		raise NotImplementedError("Implement this abstract function later.")

	def pretty_format(self, text):
		raise NotImplementedError("Implement this abstract funtion later.")