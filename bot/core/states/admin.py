from aiogram.fsm.state import State, StatesGroup

class SpamStates(StatesGroup):
    ask_photo = State()
    photo = State()
    spam_message = State()
    
class NewAdminStates(StatesGroup):
    admin_id = State()
    
class ChangeMessageStates(StatesGroup):
    message = State()