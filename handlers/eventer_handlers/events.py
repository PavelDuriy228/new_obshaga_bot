from aiogram import Router
from db import (
    Event, get_all, get_all_if
)
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import home_eventor


rt = Router()

# Активные мероприятия
@rt.callback_query(lambda c: c.data.startswith("active_events:"))
async def active_events_handl(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])    
    try:
        list_nums =await get_all_if(
            table= "Events", column="unic_kod", condition_column="status",
            condition_value="active"
        )
        event =await Event.set_by_id(id=list_nums[page])
        text = event.text 
        keyboard = []
        keyboard.append([
                InlineKeyboardButton(text="Участники", callback_data=f"followers:{list_nums[page]}"),
                InlineKeyboardButton(text="Внести правки", callback_data=f"edit_event:{list_nums[page]}")        
        ])


        # В вперед и назад
        if  page +1 < len(list_nums) and page-1 > -1:
            keyboard.append([
                InlineKeyboardButton(text="⬅️", callback_data=f"active_events:{page-1}"),
                InlineKeyboardButton(text="➡️", callback_data=f"active_events:{page+1}")        
            ])
        
        # ТОлько вперед
        if page +1 < len(list_nums) and page-1 < 0:
            keyboard.append([
                InlineKeyboardButton(text="➡️", callback_data=f"active_events:{page+1}")        
            ])
        # ТОлько назад
        if page +1 >= len(list_nums) and page-1 > -1:
            keyboard.append([
                InlineKeyboardButton(text="⬅️", callback_data=f"active_events:{page-1}")        
            ])
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await callback.message.edit_text(text = text, reply_markup=markup)
    except:
        await callback.message.edit_text(text = "Нет активных мероприятий", reply_markup=home_eventor)




# Активные мероприятия
@rt.callback_query(lambda c: c.data.startswith("all_events:"))
async def full_events(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    list_nums =await get_all(
        table='Events', column='unic_kod'
    )
    try:
        event =await Event.set_by_id(id=list_nums[page])
        text = event.text 
        text += f"\nСтатус: {event.status}"
        keyboard = []
        keyboard.append([
                InlineKeyboardButton(text="Участники", callback_data=f"followers:{list_nums[page]}")            
        ])


        # В вперед и назад
        if  page +1 < len(list_nums) and page-1 > -1:
            keyboard.append([
                InlineKeyboardButton(text="⬅️", callback_data=f"all_events:{page-1}"),
                InlineKeyboardButton(text="➡️", callback_data=f"all_events:{page+1}")        
            ])
        
        # ТОлько вперед
        if page +1 < len(list_nums) and page-1 < 0:
            keyboard.append([
                InlineKeyboardButton(text="➡️", callback_data=f"all_events:{page+1}")        
            ])
        # ТОлько назад
        if page +1 >= len(list_nums) and page-1 > -1:
            keyboard.append([
                InlineKeyboardButton(text="⬅️", callback_data=f"all_events:{page-1}")        
            ])
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await callback.message.edit_text(text = text, reply_markup=markup)
    except:
        await callback.message.edit_text(text = "Мероприятия не найдены", reply_markup= home_eventor)