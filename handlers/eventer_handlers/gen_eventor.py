from aiogram import Router
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from db import Event
from keyboards import home_eventor, eventor_markup, GetMenuForEdit
from aiogram.types import CallbackQuery, Message
from FSMs import NewEvent, SearchName
from other_func import splitter_time, search


router = Router()

@router.callback_query(lambda c: c.data == "eventor_menu")
async def eventor_menu (callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Меню действий огранизатора мероприятий", reply_markup= eventor_markup)


# Создание ивентов
@router.callback_query(lambda c: c.data == "create_event")
async def new_event (callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewEvent.name)
    await callback.message.edit_text(text="Напишите название мероприятия", reply_markup=home_eventor)

@router.message(NewEvent.name)
async def new_event1 (message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer(text="А теперь отправье описание вашего мероприятия", reply_markup=home_eventor)
    await state.set_state(NewEvent.description)
    
@router.message(NewEvent.description)
async def new_event2 (message: Message, state: FSMContext):
    await state.update_data(description = message.text)
    await message.answer(text="Осталось только дата и время нового мероприятия. Напишите дату и время по маске или по такому примеру: \n2024-10-01 14:30")
    await message.answer(text="ГГГГ-ММ-ДД ЧЧ:ММ", reply_markup=home_eventor)
    await state.set_state(NewEvent.date)

@router.message(NewEvent.date)
async def new_event3 (message: Message, state: FSMContext):
    date = await splitter_time(message.text)
    if date:        
        await state.update_data( date = message.text)
        data = await state.get_data()
        name = data['name']
        description = data['description']        

        event = await Event.setting(
            name=name,
            description=description,
            date= date[0],
            time= date[1]
        )        
        print(event.text)
        await event.add_to_table()
        await event.send_for_all()
        await message.answer(text=f"Вот что получилось: \n{name}\n\n{description}\nВ {date}", reply_markup=home_eventor)        
        await state.clear()
    else:
        await message.answer(text="Неверный формат", reply_markup=home_eventor)    

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