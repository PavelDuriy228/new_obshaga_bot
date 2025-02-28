from aiogram.fsm.state import State, StatesGroup

class StateName(StatesGroup):
    name_st = State()

class ForEditStName (StatesGroup):
    for_edit_name = State()
    new_name = State()
    
class ForDelStName (StatesGroup):
    for_del_name = State()

class NewEvent(StatesGroup):
    name = State ()
    description = State ()
    date = State()
    time_to_send = State()

class ForEditTime(StatesGroup):
    id = State()
    new_time = State()

class RebuildEvent(StatesGroup):
    id = State()
    new_name = State()
    new_discription = State()
    new_time  = State()

class MesToFolls(StatesGroup):
    id = State()
    mes = State()

class SearchName(StatesGroup):
    name = State()