from main import bot


class Database:
	def __init__(self):
		self.bot = bot

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
			'prefix VARCHAR(4) DEFAULT ;,'
		    'lyrics_source TEXT DEFAULT genius'
		    'PRIMARY KEY (guild_id)'
			');'
			)
		async with self.bot.dbpool.acquire() as conn:
			await conn.execute(command)

	async def ensure_user_properties(self):
		command = ('CREATE TABLE IF NOT EXISTS userprop('							
			'user_id BIGINT,'													
		    'brawlhalla_cog BOOLEAN DEFAULT False'
		    'PRIMARY KEY (user_id)'
			');'
			)
		async with self.bot.dbpool.acquire() as conn:
			await conn.execute(command)