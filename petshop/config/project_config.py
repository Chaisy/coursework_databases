from contextlib import asynccontextmanager
import asyncpg


class Database:
    pool = None  # Используем пул соединений вместо `connection`

    @staticmethod
    async def connect():
        try:
            # Подключаем пул
            Database.pool = await asyncpg.create_pool(
                user='postgres',
                password='1111',
                database='pet_shop',
                host='localhost',
                port=5432,
                min_size=1,  # Минимум соединений
                max_size=10,  # Максимум соединений
            )
            print("Connected to database pool.")
        except Exception as e:
            print("Error connecting to database.")
            print(e)

    @staticmethod
    async def disconnect():
        if Database.pool:
            await Database.pool.close()
            print("Database pool closed.")

    # Метод для выполнения запроса через пул
    @staticmethod
    async def execute(query: str, *args):
        async with Database.pool.acquire() as connection:
            return await connection.execute(query, *args)

    @staticmethod
    async def fetch(query: str, *args) -> list:
        async with Database.pool.acquire() as connection:
            rows = await connection.fetch(query, *args)
            return [dict(row) for row in rows]

    @staticmethod
    async def fetchrow(query: str, *args) -> dict:
        """Метод для выполнения одного запроса и получения одной строки."""
        async with Database.pool.acquire() as connection:
            row = await connection.fetchrow(query, *args)
            return dict(row) if row else None

    @staticmethod
    async def fetchval(query: str, *args):
        """Метод для выполнения запроса и возврата одного значения (первого столбца первой строки)."""
        async with Database.pool.acquire() as connection:
            row = await connection.fetchrow(query, *args)
            return row[0] if row else None