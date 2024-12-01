from typing import Optional, List

import asyncpg
from contextlib import asynccontextmanager

from schemas.schemas import User, Good


class Database:
    connection = None

    @staticmethod
    async def connect():
        try:
            Database.connection = await asyncpg.connect(
                user='postgres',
                password='1111',
                database='pet_shop',
                host='localhost',
                port=5432
            )
        except Exception as e:
            print("Something went wrong.")
            print(e)

    @staticmethod
    async def disconnect():
        if Database.connection:
            await Database.connection.close()

    @asynccontextmanager
    async def transaction(self):
        async with Database.connection.transaction():
            yield

    @staticmethod
    async def fetch_one(query: str, values: dict = None) -> dict:
        return await Database.fetch_one(query=query, values=values)





