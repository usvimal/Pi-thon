class Database:
	def __init__(self, main_loop, bot):
		self.bot = bot
		self._main_loop = main_loop
		self.task_manager()

	def task_manager(self):
		self._main_loop.create_task(self.ensure_todo_table())
		self._main_loop.create_task(self.ensure_guild_properties())
		self._main_loop.create_task(self.ensure_user_properties())

	async def ensure_todo_table(self):
		command = ('CREATE TABLE IF NOT EXISTS todotable('							
			'user_id BIGINT,'													
			'todo TEXT,'
		    'completed BOOLEAN DEFAULT False,'
		    'time_added TIMESTAMP'
			');'
			)
		async with self.bot.dbpool.acquire() as conn:
			await conn.execute(command)

	async def ensure_guild_properties(self):
		command = ('CREATE TABLE IF NOT EXISTS guildprop('
		           'guild_id BIGINT,'
		           'prefix VARCHAR(4),'
		           'PRIMARY KEY (guild_id)'
		           ');'
		           )
		async with self.bot.dbpool.acquire() as conn:
			await conn.execute(command)

	async def ensure_user_properties(self):
		command = ('CREATE TABLE IF NOT EXISTS userprop('							
			'user_id BIGINT,'													
		    'brawlhalla_cog BOOLEAN DEFAULT False,'
		    'lyrics_source TEXT DEFAULT \'genius\','
		    'PRIMARY KEY (user_id)'
			');'
			)
		async with self.bot.dbpool.acquire() as conn:
			await conn.execute(command)