from typing import Any

from aiogram.filters import BaseFilter
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from ..tools.cache import Cache
from ..tools.options import CacheOption

from ..database.repository.admin import AdminRepository

class IsAdmin(BaseFilter):
    async def __call__(
        self,
        message: Message,
        state: FSMContext
    ) -> Any:
        admins: list = await Cache.router(
            func=AdminRepository.get_objects,
            by=CacheOption.GET,
            tag='admins'
        )
        return message.from_user.id in admins
        