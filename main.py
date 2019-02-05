import discord
import os
import platform
import asyncio

from discord.ext import commands

bot = commands.Bot(command_prefix=';', pm_help=None, description='A personal project for fun')

creatorID = int(os.environ.get("creatorID"))
CillyID = int(os.environ.get("CillyID"))
WYID = int(os.environ.get("WYID"))
creator = os.environ.get("creator")


@bot.event
# outputs in log when bot is logged in
async def on_ready():
	print("*Hackerman voice* I'm in")
	print('Logged in as ' + str(bot.user.name) + ' (ID:' + str(bot.user.id) + ') | Connected to ' + str(
		len(bot.guilds)) + ' servers | Connected to ' + str(len(set(bot.get_all_members()))) + ' users')
	print('--------')
	print('Current Discord.py Version:{}|Current Python Version: {}'.format(discord.__version__,platform.python_version()))
	await bot.change_presence(activity=discord.Game(name='epic games'))
	return


async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == bot.user:
		return

	# sends message when libtard is mentioned
	if 'libtard' in message.content.lower():
		msg = 'libtard epic rekt 8)'.format(message)
		await message.channel.send(msg)
		return

	# sends thinking emoji when someone says hmm
	elif message.content.lower().startswith('hmm'):
		msg = '\U0001F914'.format(message)
		await message.channel.send(msg)
		return

	# sends ben shapiro photo when someone says ok this is epic
	if 'ok this is epic' in message.content.lower() or 'okay this is epic' in message.content.lower():
		await message.channel.send(file=discord.File('my_image.jpg'))
		return

	# sends me a message if I am mentioned
	if creator in message.content.lower():
		msg = message.content.lower().format(message)
		author = message.author
		em = discord.Embed(title='Someone messaged you!', description=msg, colour=0xFF00FF)
		em.set_author(name=author, icon_url=author.avatar_url)
		channel = bot.get_user(creatorID)
		await channel.send(embed=em)


@bot.command()
async def bot(ctx, *, arg):
	"""deletes your message and talks through the bot"""
	await ctx.delete(arg)
	print(arg.author.id)
	if arg.author.id == creatorID or arg.author.id == CillyID or arg.author.id == WYID:
		await ctx.send(arg)
		return
	else:
		await ctx.send('You are not authorised sorry! {0.author.mention}')
		return


@bot.command()
async def vote(ctx, time: int, *, reason: str):
	"""vote feature, will add reactions (thumbsup and thumbsdown) and output final result"""
	"""enter time in seconds and your reason"""
	await ctx.add_reaction('✅')
	await ctx.add_reaction('❌')
	await asyncio.sleep(time)
	reactions = (await ctx.get_message(ctx.id)).reactions
	print(reactions)
	counts = {}
	for reaction in reactions:
		counts[reaction.emoji] = reaction.count - 1
		print(f'{reaction.emoji} = {counts}')
	if counts['✅'] > counts['❌']:
		await ctx.send("The answer to" + reason + ": ✅")
	else:
		await ctx.send("The answer to" + reason + ": ❌")
		return


@bot.command
async def details(ctx):
	"""link to github"""
	em = discord.Embed(title='read my code!', url='https://github.com/usvimal/Pi-thon', colour=0xb949b5)
	em = em.set_author(name='Minininja', url='https://github.com/usvimal')
	await ctx.send(embed=em)
	return


token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)
