# -*- coding: UTF-8 -*-

import functools

import aiomysql
from aiomysql import DictCursor, Pool, create_pool

_POOL_DICT: dict[str, Pool] = dict()


async def init(name: str, **kwargs) -> None:
    _POOL_DICT[name] = await create_pool(**kwargs)


def with_mysql(*, name: str, transaction: bool = False,
               dict_cursor: bool = False):
    def decorator(f):
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):
            pool = _POOL_DICT.get(name)
            if not pool:
                raise SyntaxError(f'Pool {name} not found')
            async with pool.acquire() as connection:
                if transaction:
                    await connection.begin()
                cursor_coro = (connection.cursor(DictCursor)
                               if dict_cursor else connection.cursor())
                try:
                    async with cursor_coro as cursor:
                        kwargs['cursor'] = cursor
                        result = await f(*args, **kwargs)
                    await connection.commit()
                except Exception as e:
                    await connection.rollback()
                    raise e
                return result
        return wrapper

    return decorator
