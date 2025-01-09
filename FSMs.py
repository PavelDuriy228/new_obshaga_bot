from aiogram.fsm.state import State, StatesGroup

class StateName(StatesGroup):
    name_st = State()

class ForEditStName (StatesGroup):
    for_edit_name = State()
    new_name = State()
    
class ForDelStName (StatesGroup):
    for_del_name = State()