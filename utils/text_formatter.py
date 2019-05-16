"""
Used for chunking pieces of text to work around Discord's message size limit
Message limit: 2,000 characters. (note: user/channel/role mentions and emojis contain more characters than are shown)
"""


def chunks(s, n):
	"""Produce `n`-character chunks from `s`."""
	for start in range(0, len(s), n):
		yield s[start:start + n]


def strike(text):
	result = ''
	for c in text:
		result = result + c + '\u0336'
	return result