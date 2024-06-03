from typing import Any, Awaitable, Callable, Coroutine, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, ChatJoinRequest, ChatMemberUpdated

from ..database.repository.users import UserRepository
from ..tools.cache import Cache


class NewUserMiddleware(BaseMiddleware):
        
    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: Union[ChatMemberUpdated, ChatJoinRequest], 
        data: Dict[str, Any]
    ) -> Coroutine[Any, Any, Any]:
        print("In NewUser")
        await Cache.invaliding_cache(
            tag="users"
        )
        try:
            await UserRepository.insert_object(
                data={
                    "telegram_id": event.from_user.id
                }
            )
        except Exception as e:
            print(e)
        return await handler(event, data)