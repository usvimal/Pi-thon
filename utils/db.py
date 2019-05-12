import asyncpg
import config
import ssl


ctx = ssl.create_default_context(cafile='assets/rds-combined-ca-bundle.pem')
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
postgres_connection = await asyncpg.connect(dsn=config.DATABASE_URL, ssl=ctx)


async def ensure_todo_table():
	await postgres_connection.execute(' CREATE TABLE IF NOT EXISTS todotable('
	                                  'user_id BIGINT DEFAULT 0, '
	                                  'to-do TEXT, CONSTRAINT to-do_pk '
	                                  'PRIMARY KEY (user_id) )')
