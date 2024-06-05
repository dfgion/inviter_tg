from typing import Any, Awaitable, Callable, Coroutine, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, ChatJoinRequest, ChatMemberUpdated

from ..database.repository.admin import AdminRepository

from ..tools.cache import Cache
from ..tools.options import CacheOption

class IsAdminMiddleware(BaseMiddleware):
        
    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: Union[ChatMemberUpdated, ChatJoinRequest], 
        data: Dict[str, Any]
    ) -> Coroutine[Any, Any, Any]:
        admins: list = await Cache.router(
            func=AdminRepository.get_objects,
            by=CacheOption.GET,
            tag='admins'
        )
        if event.from_user.id in admins:
            return await handler(event, data)