from aiogram import Router, Bot
from aiogram.types import (
    ChatJoinRequest,
    ChatMemberUpdated
)
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, JOIN_TRANSITION

from ..markups.inline import invitation_channels_keyboard

from ..tools.cache import Cache
from ..tools.options import CacheOption

from ..database.repository.message import MessageRepository

router = Router()

@router.chat_join_request()
async def approve_user(chat_join: ChatJoinRequest, bot: Bot):
    messages = await Cache.router(
        func=MessageRepository.get_objects,
        by=CacheOption.GET,
        tag='messages'
    )
    await bot.send_message(
        chat_id=chat_join.from_user.id,
        text=messages[0],
        parse_mode='html',
        reply_markup=invitation_channels_keyboard()
    )
    

@router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def handle_public_join(event: ChatMemberUpdated, bot: Bot):
    messages = await Cache.router(
        func=MessageRepository.get_objects,
        by=CacheOption.GET,
        tag='messages'
    )
    await bot.send_message(
        chat_id=event.from_user.id,
        text=messages[0],
        parse_mode='html',
        reply_markup=invitation_channels_keyboard()
    )