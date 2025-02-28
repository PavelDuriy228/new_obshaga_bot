from aiogram import Router
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from db import Event
from keyboards import home_eventor, eventor_markup, GetMenuForEdit
from aiogram.types import CallbackQuery, Message
from FSMs import NewEvent, SearchName
from other_func import splitter_time, search
from config import scheduler
from datetime import datetime


router = Router()

@router.callback_query(lambda c: c.data == "eventor_menu")
async def eventor_menu (callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Меню действий огранизатора мероприятий", reply_markup= eventor_markup)


# Создание ивентов
@router.callback_query(lambda c: c.data == "create_event")
async def new_event (callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewEvent.name)
    await callback.message.edit_text(
        text="Напишите название мероприятия", 
        reply_markup=home_eventor
    )

@router.message(NewEvent.name)
async def new_event2 (message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer(
        text="Теперь введите дату и время нового мероприятия. \
        Напишите дату и время по маске или по такому примеру: \n2024-10-01 14:30"
    )
    await message.answer(text="ГГГГ-ММ-ДД ЧЧ:ММ", reply_markup=home_eventor)
    await state.set_state(NewEvent.date)

@router.message(NewEvent.date)
async def new_event1 (message: Message, state: FSMContext):
    date = await splitter_time(message.text)
    if date:        
        await state.update_data( date = message.text)
        await message.answer(
            text="Напишите когда во сколько нужно будет отправить сообщение"            
        )
        await message.answer(text="ГГГГ-ММ-ДД ЧЧ:ММ", reply_markup=home_eventor)
        await state.set_state(NewEvent.time_to_send)
    else:
        await message.answer(text="Неверный формат", reply_markup=home_eventor)        
    
@router.message(NewEvent.time_to_send)
async def new_event1 (message: Message, state: FSMContext):
    date = await splitter_time(message.text)
    if date:        
        await state.update_data( time_to_send = message.text)
        await message.answer(
            text="Теперь отправьте описание вашего мероприятия",         
            reply_markup=home_eventor
        )
        await state.set_state(NewEvent.description)
    else:
        await message.answer(text="Неверный формат", reply_markup=home_eventor)            

@router.message(NewEvent.description)
async def new_event3 (message: Message, state: FSMContext):    
    await state.update_data( description = message.text)
    data = await state.get_data()
    name = data['name']
    description = data['description']
    time_to_send = data['time_to_send']        
    date = str(data['date']).strip().split(" ")
    event = await Event.setting(
        name=name,
        description=description,
        date= date[0],
        time= date[1]
    )        
    print(event.text)

    await event.add_to_table()

    time_to_send = datetime.strptime(
        time_to_send, "%Y-%m-%d %H:%M"
    )
    scheduler.add_job(
        event.send_for_all,
        trigger='date',
        run_date = time_to_send,
        args=[message]
    )
    
    await message.answer(text=f"Вот что получилось: \n{name}\n\n{description}\nВ {date}", reply_markup=home_eventor)        
    await state.clear()
    

@router.callback_query(lambda c: c.data == "search_event")
async def search_event (callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchName.name)
    await callback.message.edit_text(
        text="Введите название мероприятия",
        reply_markup= home_eventor
    )

@router.message(SearchName.name)
async def searching(message: Message, state: FSMContext):
    id =await search(query=message.text)
    event = await Event.set_by_id(id=id)
    markup = await GetMenuForEdit(id =id)
    await message.answer(
        text= f"Наиболее совпавшее мероприятие\n{event.text}",
        reply_markup=markup
    )