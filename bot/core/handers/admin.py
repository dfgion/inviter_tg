import asyncio

from aiogram import Router, F 
from aiogram.types import (
    Message, 
    CallbackQuery, 
)
from aiogram.fsm.context import FSMContext

from ..markups.inline import (
    admin_menu_keyboard, accept_spam_message_keyboard, 
    back_to_menu_keyboard, accept_new_admin_keyboard, 
    ask_photo_keyboard, accept_changing_keyboard
)
from ..filters.chat import ChatTypeFilter
from ..filters.admin import IsAdmin

from ..tools.cache import Cache
from ..tools.options import CacheOption

from ..database.repository.admin import AdminRepository
from ..database.repository.users import UserRepository
from ..database.repository.message import MessageRepository

from ..states.admin import (
    SpamStates, NewAdminStates, ChangeMessageStates
)

from ..config import bot


router = Router()


@router.callback_query(F.data == 'add_photo')    
async def ask_photo_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        text="Пришлите фотографию для рассылки"
    )
    try:
        await callback_query.message.delete()
    except:
        pass
    
@router.message(F.content_type == 'photo', SpamStates.photo)      
@router.callback_query(F.data == 'ask_confirm')
async def ask_confirm_spam(invoice: CallbackQuery | Message, state: FSMContext):
    if hasattr(invoice, "data"):
        message = invoice.message
    else:
        await state.update_data(
            {
                "photo_id": invoice.photo[2].file_id
            }
        )
        message = invoice
    await message.answer(
        text="Вы уверены, что хотите отправить это сообщение?",
        reply_markup=accept_spam_message_keyboard()
    )
    try:
        await message.delete()
    except:
        pass
    
@router.message(F.content_type == 'photo', ChangeMessageStates.photo)      
@router.callback_query(F.data == 'ask_confirm')
async def ask_confirm_spam(invoice: CallbackQuery | Message, state: FSMContext):
    if hasattr(invoice, "data"):
        message = invoice.message
    else:
        await state.update_data(
            {
                "photo_id": invoice.photo[2].file_id
            }
        )
        message = invoice
    await message.answer(
        text="Вы уверены, что хотите изменить сообщение?",
        reply_markup=accept_changing_keyboard()
    )
    try:
        await message.delete()
    except:
        pass
    
@router.message(ChangeMessageStates.message) 
async def new_message_handler(message: Message, state: FSMContext):
    await message.answer(
        text="Вы хотите добавить фото к сообщению?",
        reply_markup=ask_photo_keyboard()
    )
    await state.update_data(
        {
            "change_message": message.text
        }
    )
    await state.set_state(ChangeMessageStates.photo)

@router.message(SpamStates.spam_message)    
async def handle_spam_message(message: Message, state: FSMContext):
    await state.update_data(
        {
            "spam_message": message.text
        }
    )
    await message.reply(
        text="Хотите добавить фотографию к этому сообщению?",
        reply_markup=ask_photo_keyboard()
    )
    await state.set_state(SpamStates.photo)

@router.message(NewAdminStates.admin_id)
async def handle_admin_id(message: Message, state: FSMContext):
    try:
        if (message.text and (len(message.text.strip()) <= 19)):
            await state.update_data(
                {
                    "admin_telegram_id": int(message.text.strip())
                }
            )
            await message.answer(
                text="Вы уверены, что хотите назначиить данного пользователя администратором?",
                reply_markup=accept_new_admin_keyboard()
            )
        else:
            raise Exception()
    except:
        await message.answer(
                text="Некорректный ответ, введите корректный telegram id администратора"
            )

@router.message(ChatTypeFilter(chat_type=['private']), IsAdmin())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Здравствуйте, {name}".format(name=message.from_user.full_name),
        reply_markup=back_to_menu_keyboard()
    )
    
    
@router.callback_query(F.data == 'menu')
async def menu_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.answer(
        text="Выберите действие ниже",
        reply_markup=admin_menu_keyboard()
    )
    try:
        await callback_query.message.delete()
    except:
        pass
   
    
@router.callback_query(F.data == 'assign_admin')
async def start(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        text="Введите telegram_id пользователя"
    )
    await state.set_state(NewAdminStates.admin_id)
    try:
        await callback_query.message.delete()
    except:
        pass
    
    
@router.callback_query(F.data == 'spam')
async def start(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        text="Введите сообщение для рассылки пользователям"
    )
    await state.set_state(SpamStates.spam_message)
    try:
        await callback_query.message.delete()
    except:
        pass
 
 
@router.callback_query(F.data == 'accept_new_admin')
async def accept_new_admin(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    admin_id = data.get("admin_telegram_id")
    await Cache.invaliding_cache(
        tag="admins"
    )
    await AdminRepository.insert_object(
        data={
            "telegram_id": admin_id
        }
    )
    await callback_query.message.answer(
        text="Пользователь с telegram_id {admin_id} теперь новый администратор и может пользоваться функциями как и Вы".format(admin_id=admin_id)
    )
    try:
        await callback_query.message.delete()
    except:
        pass
    
    

@router.callback_query(F.data == 'start_spam')    
async def start_spam(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if telegram_ids := await Cache.router(
        func=UserRepository.get_objects,
        by=CacheOption.GET,
        tag='users'
    ):  
        text = data.get("spam_message")
        for telegram_id in telegram_ids:
            if photo_id := data.get("photo_id"):
                await bot.send_photo(
                    chat_id=telegram_id,
                    photo=photo_id,
                    caption=text
                )
            else:
                await bot.send_message(
                    chat_id=telegram_id,
                    text=text
                )
        try:
            await callback_query.message.edit_text(
                text="Рассылка запущена",
                reply_markup=back_to_menu_keyboard()
            )
        except:
            pass
    else:
        await callback_query.message.edit_text(
            text="Пока нет пользователей для рассылки",
            reply_markup=back_to_menu_keyboard()
        )
    
        

@router.callback_query(F.data == 'change_join_message')
async def change_join_message_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Напишите сообщение, которое будет отправляться пользователям при отправке заявки на вступление в канал")
    await state.set_state(ChangeMessageStates.message)
    try:
        await callback_query.message.delete()
    except:
        pass
    

@router.callback_query(F.data == 'accept_changing')
async def accept_changing_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await MessageRepository.update_object(
        entry_id=1,
        data={
            "text": data.get("change_message"),
            "photo_id": data.get("photo_id")
        }
    )
    await Cache.invaliding_cache(
        tag='messages'
    )
    await callback_query.message.answer("Сообщение было изменено")
    try:
        await callback_query.message.delete()
    except:
        pass