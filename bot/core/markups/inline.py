from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_menu_keyboard():
    inline_keyboard = InlineKeyboardBuilder()
    
    buttons = [
        {"text": "Назначить администратора", "callback_data": "assign_admin"},
        {"text": "Рассылка", "callback_data": "spam"},
        {"text": "Изменить первое сообщение", "callback_data": "change_join_message"},
    ]
    
    for button in buttons:
        inline_keyboard.add(InlineKeyboardButton(**button))
        
    inline_keyboard.adjust(1, 1, 1)
    
    return inline_keyboard.as_markup()

def invitation_channels_keyboard(without_check: bool = False):
    inline_keyboard = InlineKeyboardBuilder()
    
    buttons = [
        {"text": "Авторынок", "url": "https://t.me/+7-R5GjC5_sRmNWQy"},
        {"text": "ГИБДД", "url": "https://t.me/+knJo_8in22NlZWQy"},
        {"text": "Турне по России", "url": "https://t.me/+xdqt-R873LY4MGZi"},
        check := {"text": "Проверить", "callback_data": "checking_for_subscription"}
    ]
    if not without_check:
        buttons.pop(buttons.index(check))
    for button in buttons:
        inline_keyboard.add(InlineKeyboardButton(**button))
        
    inline_keyboard.adjust(3, 1)
    
    return inline_keyboard.as_markup()

def accept_spam_message_keyboard():
    inline_keyboard = InlineKeyboardBuilder()
    
    buttons = [
        {"text": "Да, начать рассылку", "callback_data": "start_spam"},
        {"text": "Нет, отменить", "callback_data": "menu"}
    ]
    
    
    for button in buttons:
        inline_keyboard.add(InlineKeyboardButton(**button))
        
    inline_keyboard.adjust(1, 1)
    
    return inline_keyboard.as_markup()

def accept_new_admin_keyboard():
    inline_keyboard = InlineKeyboardBuilder()
    
    buttons = [
        {"text": "Да, назначить", "callback_data": "accept_new_admin"},
        {"text": "Нет, не назначать", "callback_data": "menu"}
    ]
    
    
    for button in buttons:
        inline_keyboard.add(InlineKeyboardButton(**button))
        
    inline_keyboard.adjust(1, 1)
    
    return inline_keyboard.as_markup()


def back_to_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Меню", callback_data="menu")
            ]
        ]
    )
    
def ask_photo_keyboard():
    inline_keyboard = InlineKeyboardBuilder()
    
    buttons = [
        {"text": "Нет, не хочу", "callback_data": "ask_confirm"},
        {"text": "Да, хочу добавить", "callback_data": "add_photo"}
    ]
    
    
    for button in buttons:
        inline_keyboard.add(InlineKeyboardButton(**button))
        
    inline_keyboard.adjust(1, 1)
    
    return inline_keyboard.as_markup()

def accept_changing_keyboard():
    inline_keyboard = InlineKeyboardBuilder()
    
    buttons = [
        {"text": "Нет, не изменять", "callback_data": "menu"},
        {"text": "Да, хочу изменить", "callback_data": "accept_changing"}
    ]
    
    
    for button in buttons:
        inline_keyboard.add(InlineKeyboardButton(**button))
        
    inline_keyboard.adjust(1, 1)
    
    return inline_keyboard.as_markup()