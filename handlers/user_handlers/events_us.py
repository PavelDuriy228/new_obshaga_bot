from aiogram import  Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from db import Event, get_value_by_condition
from other_func import replacer
from keyboards.strelki import create_strelki

router = Router()

@router.callback_query(lambda c: c.data.startswith("join:"))
async def joining (callback: CallbackQuery):
    # id мероприятия
    id = int(callback.data.split(":")[1])
    event = await Event.set_by_id(id=id)

    user_id = callback.from_user.id
    username = callback.from_user.username
    
    #  ДОбавлет новое значение к уже сущщетсвующим (В столбце с ивентами добавляет ид нового)
    await replacer(
        table="Users", column="codes_events", condition_column='tg_id',
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
        text= f"Теперь вы следите за мероприятием \n{event.name}"        
    )

@router.callback_query(lambda c: c.data.startswith("users_events:"))
async def joining (callback: CallbackQuery):
    id = callback.from_user.id
    event_codes = str (await get_value_by_condition(
        table="Users",
        column='codes_events',
        condition_column='tg_id', condition_value=id  
    )).strip()
    page= int(callback.data.split(":")[2])    
    keyboard = []
    keyboard.append(
        [InlineKeyboardButton(text="🏠Домой", callback_data=f"home_stud:{id}")]
    )    

    if event_codes !="None": list_id = [code.strip() for code in event_codes.split(" ") if code != ""]  
    if list_id and len(list_id)>0:                
        print(list_id)          
        try:            
            event = await Event.set_by_id(id=list_id[page])
            text = event.text            
            keyboard.append(
                [InlineKeyboardButton(text="Отменить запись", callback_data=f"user_otmena:{id}:{list_id[page]}")]
            )
        except Exception as e:
            text="Возможно такого мероприятия не существует"
        
        strelki = await create_strelki(
            len_list=len(list_id), 
            callback_dataU=f"users_events:{id}",
            page= page
        )
        if strelki: keyboard.append(strelki)
        
    else:
        text="записей на мероприятия нет"
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.edit_text(text=text,reply_markup= markup)

@router.callback_query(lambda c: c.data.startswith("user_otmena:"))
async def joining (callback: CallbackQuery):
    id = callback.from_user.id
    id_event= int(callback.data.split(":")[2])

    event = await Event.set_by_id(id=id_event)
    # Замена в таблице Just_users в колонке с его ивентами id выбранного id на пустоту
    await replacer(
        table="Users", column="codes_events", condition_column='tg_id',
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

    await callback.message.answer(text = f"Вы больше не следите за этим мероприятием\n{event.name}")