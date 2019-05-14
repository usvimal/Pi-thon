from discord.ext import commands
from utils.db import postgres_connection

class Personal_todo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def get_user_todos(self, user_id: int):
		row = await postgres_connection.fetchrow(f"SELECT todo FROM todotable WHERE user_id = $1;",
		                                         user_id)

		if row is None:
			return None
		return row["todo"]

	@commands.group()
	async def todo(self, ctx):
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed:
				await ctx.send('Oof owie, that was not a valid command 🤨')
			else:
				author_todo = await self.get_user_todos(ctx.author.id)
				if author_todo is None:
					await ctx.send("You have nothing to do")
				else:
					await ctx.send("Here are your to-dos: \n" + author_todo)

	@todo.command()
	async def add(self, ctx, new_todo: str):
		user_id = ctx.author.id
		current_todos = await self.get_user_todos(user_id)
		if current_todos is None:
			await postgres_connection.execute(
				f"INSERT INTO todotable VALUES ($1, $2) ON CONFLICT (user_id) DO "
				f"UPDATE SET todo = $2;",
				user_id, new_todo)
		else:
			await postgres_connection.execute(
				f"INSERT INTO todotable VALUES ($1, $2) ON CONFLICT (user_id) DO "
				f"UPDATE SET todo = $2;",
				user_id, current_todos + '\n' + new_todo)




def setup(bot):
		bot.add_cog(Personal_todo(bot))
