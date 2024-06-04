from aiogram.fsm.state import State, StatesGroup

class SpamStates(StatesGroup):
    spam_message = State()
    photo = State()
    
class NewAdminStates(StatesGroup):
    admin_id = State()
    
class ChangeMessageStates(StatesGroup):
    message = State()
    photo = State()