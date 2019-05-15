import asyncio
import asyncpg
import config
import ssl


ctx = ssl.create_default_context(cafile='assets/rds-combined-ca-bundle.pem')
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
conn_pool = None


async def init_postgres_connection():
	global conn_pool
	conn_pool = await asyncpg.create_pool(dsn=config.DATABASE_URL)
asyncio.get_event_loop().run_until_complete(init_postgres_connection())


async def ensure_todo_table():
	command = ('CREATE TABLE IF NOT EXISTS todotable('							
		'user_id BIGINT DEFAULT 0,'													
		'todo TEXT,'
	    'completed BOOLEAN DEFAULT False'
		');'
		)
	async with conn_pool.acquire() as conn:
		await conn.execute(command)
