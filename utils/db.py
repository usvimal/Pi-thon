import asyncio
import asyncpg
import config
import ssl


ctx = ssl.create_default_context(cafile='assets/rds-combined-ca-bundle.pem')
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
postgres_connection = None


async def _init_postgres_connection():
	global postgres_connection
	postgres_connection = await asyncpg.connect(dsn=config.DATABASE_URL, ssl=ctx)

asyncio.get_event_loop().create_task(_init_postgres_connection())


async def ensure_todo_table():
	command = ('CREATE TABLE IF NOT EXISTS todotable('
														'user_id BIGINT DEFAULT 0,'
														'to-do TEXT,'
														'CONSTRAINT to-do_pk,'
														'PRIMARY KEY (user_id)'
													')'
																					)
	await postgres_connection.execute(command)
