import discord

from discord.ext import commands
from utils.db import conn_pool


class personal_todo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def get_user_todos(self, user_id: int):
		async with conn_pool.acquire() as conn:
			details = await conn.fetch(f"SELECT todo, completed FROM todotable WHERE user_id = $1;",
		                                            user_id)
		if details is None:
			return None
		return details

	@staticmethod
	def convert_boolean_to_emoji(dict_to_convert):
		for key, item in dict_to_convert.items():
			if item is False:
				dict_to_convert[key] = '❌'
			if item is True:
				dict_to_convert[key] = '✅'

	@commands.group()
	async def todo(self, ctx):
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed:
				await ctx.send('Oof owie, that was not a valid command 🤨')
			else:
				todo_record = await self.get_user_todos(ctx.author.id)
				if todo_record is None:
					await ctx.send(f"{ctx.user.mention} has no todos yet.")
				else:
					todo_dict = dict(todo_record)
					em = discord.Embed(title='To-dos', colour=0xff3056)
					em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
					self.convert_boolean_to_emoji(todo_dict)
					for key, value in todo_dict.items():
						em.add_field(name=key, value=value, inline=False)
					await ctx.send(embed=em)

	@todo.command()
	async def add(self, ctx, *, new_todo: str):
		user_id = ctx.author.id
		async with conn_pool.acquire() as conn:
			await conn.execute(
				f"INSERT INTO todotable VALUES ($1, $2)"
				,user_id, new_todo)
		await ctx.message.add_reaction('👍')


def setup(bot):
	bot.add_cog(personal_todo(bot))
