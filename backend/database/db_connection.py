from asyncpg.connection import connect

async def get_database_connection():
    return await connect(
        host='localhost',
        port=5432,
        user='postgres',
        password='12345',
        database='recipes_pr_db'
    )
