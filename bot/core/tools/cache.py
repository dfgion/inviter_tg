import pickle
from typing import Awaitable

import redis.asyncio as aioredis
from redis.asyncio.client import Redis

from .options import CacheOption
from .exceptions import ByException


from ..config import Config
from ..schemas.basic import ResultItems


class Cache:
    
    @classmethod
    async def router(
        cls, 
        *, 
        func: Awaitable[list], 
        by: CacheOption, 
        **kwargs
    ):
        r = await aioredis.from_url(Config.REDIS_DSN)
        match by:
            case CacheOption.GET:
                result = await cls.__get_objects(
                    func=func, 
                    r=r,
                    tag=kwargs.get("tag")
                )
            case _:
                raise ByException("Unsupported method of by")
        await r.aclose()
        return result
    
    
    @classmethod    
    async def __get_objects(
        cls, 
        *, 
        func: Awaitable[ResultItems], 
        r: Redis,
        tag: str
    ):
        if (result := await r.get(tag)):
            return pickle.loads(result)
        else:
            result = await func()
            await r.set(
                name=tag,
                value=pickle.dumps(result)
            )
            return result
    
    
    @classmethod
    async def invaliding_cache(
        cls,
        tag: str
    ):
        r = await aioredis.from_url(Config.REDIS_DSN)
        try:
            await r.unlink(tag)
        except:
            pass
        finally:
            await r.aclose()