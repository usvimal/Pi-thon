import asyncio
import discord
import owotrans

from discord.ext import commands
from utils.checks import is_approved_talker


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def owo(self, ctx, *, arg):
		"""owoifies your message"""
		msg = owotrans.owo(arg)
		await ctx.send(msg)

	@commands.command(aliases=["say"])
	@is_approved_talker()
	@commands.bot_has_permissions(manage_messages=True)
	async def talk(self, ctx, *, arg):
		"""deletes your message and talks through the bot"""
		await ctx.message.delete()
		await ctx.send(arg)

	@commands.command()
	async def dice(self, ctx):
		""" Roll the dice until you die (roll 4 to 6). """
		from random import randint

		# Delete message which invoked this command
		await ctx.message.delete()

		game_in_progress = True
		round_number = 1
		accumulated_score = 0

		# Initialise the reactions, message
		roll_emoji = "\U0001F3B2"
		stop_emoji = "\U0000274E"
		embed = discord.Embed(title="Dice Game")
		embed.description = f"| Player : {ctx.author.name} | Round : {round_number} | Game In Progress |"
		embed.add_field(name="Score", value=str(accumulated_score), inline=False)
		embed.set_footer(text=f"{roll_emoji} to keep rolling, {stop_emoji} to end game and keep your score")

		# Show the message
		message = await ctx.send(embed=embed)
		await message.add_reaction(roll_emoji)
		await message.add_reaction(stop_emoji)

		# This function will handle user input
		def progress(reaction, user):
			nonlocal user_choice
			# If the user is not the player or the reaction is not on the correct message, ignore
			if (user is None) or (user.id != ctx.author.id) or (reaction.message.id != message.id):
				user_choice = None
				return False

			if reaction.emoji == roll_emoji:
				user_choice = roll_emoji

			elif reaction.emoji == stop_emoji:
				user_choice = stop_emoji

			return True


		# The game starts here
		user_choice = None			# Stores the user choice made in each iteration of the while loop
		while game_in_progress:
			try:
				curr_reaction, curr_user = await ctx.bot.wait_for('reaction_add', check=progress, timeout=60.0)
				await message.remove_reaction(curr_reaction, curr_user)
			except asyncio.TimeoutError:
				user_choice = None
				game_in_progress = False
				await message.delete()
				await ctx.send(f"`Dice Game: {ctx.author.name} timed out with a score of {accumulated_score} on Round {round_number}.`")
			except Exception as e:
				pass			# Choose to ignore this error

			# The player chooses to roll again
			if user_choice is roll_emoji:
				round_number += 1
				roll = randint(1, 6)

				if roll <= 3:		# The player rolls successfully, the score will be added
					accumulated_score += roll
					embed.description = f"| Player : {ctx.author.name} | Round : {round_number} | Game In Progress |"
					embed.set_field_at(0, name="Score", value=f"You rolled a {roll}. Your new score is {accumulated_score}.")
					await message.edit(embed=embed)
				else:				# The player rolls more than 3 and die
					game_in_progress = False
					await message.delete()
					await ctx.send(f"`Dice Game: {ctx.author.name} rolled a {roll} and lost with a score of {accumulated_score} on Round {round_number}`")

			# The player chooses to stop
			elif user_choice is stop_emoji:
				game_in_progress = False
				await message.delete()
				await ctx.send(f"`Dice Game: {ctx.author.name} kept a score of {accumulated_score} on Round {round_number}`")


def setup(bot):
	bot.add_cog(Fun(bot))
