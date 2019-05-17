from discord.ext import commands
import config


def is_officer():
    def predicate(ctx):
        return ctx.message.author.id == config.MinID or config.creatorID
    return commands.check(predicate)
