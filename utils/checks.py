from discord.ext import commands
import config


def is_officer():
    def predicate(ctx):
        return ctx.message.author.id == config.MinID or config.creatorID
    return commands.check(predicate)


def in_hideout_task_channel():
    async def predicate(ctx):
        return ctx.guild.id == 572561960982413334
    return commands.check(predicate)
