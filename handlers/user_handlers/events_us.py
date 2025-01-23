from aiogram import  Router
from keyboards import total_statistik, start_inl_kbs
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from db import Event, update_value_w_symbol, get_value_by_condition, update_value
from other_func import replacer

router = Router()

@router.callback_query(lambda c: c.data.startswith("join:"))
async def joining (callback: CallbackQuery):
    id = int(callback.data.split(":")[1])
    

    user_id = callback.from_user.id
    username = callback.from_user.username
    
    #  ДОбавлет новое значение к уже сущщетсвующим (В столбце с ивентами добавляет ид нового)
    await replacer(
        table="Just_users", column="code_events", condition_column='unic_kod',
        condition_value=user_id, value_for_replace='_52nothing52_', value_to_replace=id
    )
    #  ДОбавлет новое значение к уже сущщетсвующим (В столбце с ивентами добавляет ид нового
    await replacer(
        table="Events", column="joined_users_id", condition_column='unic_kod',
        condition_value=id, value_for_replace='_52nothing52_', value_to_replace=user_id
    )
    await replacer (
        table="Events", column="joined_users_username", condition_column='unic_kod',
        condition_value=id, value_for_replace='_52nothing52_', value_to_replace=username
    )    

    await callback.message.edit_text(
        text= "Теперь вы следите за мероприятием"        
    )

@router.callback_query(lambda c: c.data.startswith("users_events:"))
async def joining (callback: CallbackQuery):
    id = int(callback.data.split(":")[1])
    list_id = await get_value_by_condition(
        table="Just_users",
        column='code_events',
        condition_column='unic_kod', condition_value=id  
    )
    page= int(callback.data.split(":")[2])
    keyboard = []
    keyboard.append(
        [InlineKeyboardButton(text="🏠Домой", callback_data=f"home_stud:{id}")]
    )

    if list_id:
        try:
            event = await Event.set_by_id(id=list_id[page])
            text = event.text
            keyboard.append(
                [InlineKeyboardButton(text="Отменить запись", callback_data=f"user_otmena:{id}:{list_id[page]}")]
            )
            # Вперед и назад
            if page+1<len(list_id) and page-1>-1:
                keyboard.append([
                    InlineKeyboardButton(text="⬅️", callback_data=f"users_events:{id}:{page-1}"),
                    InlineKeyboardButton(text="➡️", callback_data=f"users_events:{id}:{page+1}")        
                ])
            # ТОлько вперед
            if page +1 < len(list_id) and page-1 < 0:
                keyboard.append([
                    InlineKeyboardButton(text="➡️", callback_data=f"users_events:{page+1}")        
                ])
            # ТОлько назад
            if page +1 >= len(list_id) and page-1 > -1:
                keyboard.append([
                    InlineKeyboardButton(text="⬅️", callback_data=f"users_events:{page-1}")        
                ])            
        except Exception as e:
            text="Возможно такого мероприятия не существует"
    else:
        text="None"
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.edit_text(text=text,reply_markup= markup)

@router.callback_query(lambda c: c.data.startswith("user_otmena:"))
async def joining (callback: CallbackQuery):
    id = int(callback.data.split(":")[1])
    id_event= int(callback.data.split(":")[2])

    # Замена в таблице Just_users в колонке с его ивентами id выбранного id на пустоту
    await replacer(
        table="Just_users", column="code_events", condition_column='unic_kod',
        condition_value=id, value_for_replace=id_event, value_to_replace=''
    )
    # ЗАмена в таблице ивентов id следящего за мероприятием юзера на ""
    await replacer(
        table="Events", column="joined_users_id", condition_column='unic_kod',
        condition_value=id_event, value_for_replace=id, value_to_replace=''
    )
    # Замена в таблице ивентов username
    await replacer(
        table="Events", column="joined_users_username", condition_column='unic_kod',
        condition_value=id_event, value_for_replace=callback.from_user.username, 
        value_to_replace=''
    )

    await callback.message.answer(text = "Вы больше не следите за этим мероприятием")