from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, is_superuser, phone_number, telegram_id, full_name, is_staff, daily_use,confirm_code, created_at):
        sql = "INSERT INTO accounts_user (password, is_superuser, phone_number, telegram_id, full_name, is_staff, daily_use,confirm_code, created_at) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) returning *"
        return await self.execute(sql, telegram_id, is_superuser, phone_number, telegram_id, full_name, is_staff, daily_use,confirm_code, created_at, fetchrow=True)

    async def update_user_confirm_code(self, confirm_code, telegram_id):
        sql = "UPDATE accounts_user SET confirm_code=$1 WHERE telegram_id=$2"
        return await self.execute(sql, confirm_code, telegram_id, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM accounts_user"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM accounts_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        data = await self.execute(sql, *parameters, fetchrow=True)
        return {
            "id": data[0],
            "phone_number": data[4],
            "full_name": data[6],
            "created_at": data[9]
        } if data else None

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def add_attempt(self, audio, created_at, user_id, audio_code):
        sql = "INSERT INTO speech2text_attempt (audio, created_at, user_id, audio_code) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, audio, created_at, user_id, audio_code, fetchrow=True)
