from discord.ext import commands
import config


def is_officer():
    def predicate(ctx):
        return ctx.message.author.id == config.MinID or config.creatorID
    return commands.check(predicate)


def in_hideout_task_channel():
    def predicate(ctx):
        return ctx.channel.id == 572561960982413334
    return commands.check(predicate)
