from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: str | list):
        self.chat_type = chat_type

    async def __call__(self, update: Message | CallbackQuery) -> bool:
        if isinstance(update, CallbackQuery):
            current_chat_type = update.message.chat.type
        else:
            current_chat_type = update.chat.type
        if isinstance(self.chat_type, str):
            return current_chat_type == self.chat_type
        else:
            return current_chat_type in self.chat_type