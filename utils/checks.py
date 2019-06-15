import config
from discord.ext import commands

def is_approved_talker():
	def predicate(ctx):
		author_id = ctx.message.author.id
		return author_id == config.creatorID or author_id == config.CillyID or author_id == config.WYID or author_id == config.MinID
	return commands.check(predicate)
