from aiogram import Router
from db import (
    Event
)
from keyboards import GetMenuForEdit, home_eventor
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from FSMs import ForEditTime, RebuildEvent, MesToFolls
from other_func import  splitter_time


rt = Router()

# Просмотр подписанных
@rt.callback_query(lambda c: c.data.startswith("followers:"))
async def see_folowers (callback: CallbackQuery):
    id = int(callback.data.split(":")[1])
    event =await Event.set_by_id(id=id)
    text = "Вот список тех, кто следит за событием"
    if event: 
        followers = event.joined_users_username.split(" ")   
        print(followers)         
        for follower in followers:
            if follower != "None": text += f"\n@{follower}"
    else : text+="None"
    await callback.message.answer(text=text)

# Выбор меню для редактирования
@rt.callback_query(lambda c: c.data.startswith("edit_event:"))
async def menu_for_edit(callback: CallbackQuery):
    id = int(callback.data.split(":")[1])
    markup = await GetMenuForEdit(id=id)    
    await callback.message.answer(text="Выберите, то что вы хотите изменить", reply_markup=markup)


# Отмена мероприятия
@rt.callback_query(lambda c: c.data.startswith("otmena:"))
async def otmena_event(callback: CallbackQuery):
    id = int(callback.data.split(":")[1])
    event =await Event.set_by_id(id=id)
    # Смена статуса ивента
    await event.diactivate()
    await callback.message.edit_text(text= "Мероприятие отмененно, сообщение об отменен было отправленно следящим")


@rt.callback_query(lambda c: c.data.startswith("edit_time:"))
async def otmena_event(callback: CallbackQuery, state: FSMContext):
    id = int(callback.data.split(":")[1])
    await state.set_state(ForEditTime.id)
    await state.update_data(id = id)
    await state.set_state(ForEditTime.new_time)
    event =await Event.set_by_id(id=id)
    await callback.message.edit_text(
        text= f"Введите новое время. Вот пример:\n2024-10-01 14:30 \nТекущее: {event.date} {event.time}",
        reply_markup= home_eventor
    )

@rt.message(ForEditTime.new_time)
async def set_new_time(message: Message, state: FSMContext):
    date = await splitter_time(date = message.text)
    if date:        
        await state.update_data(new_time = message.text)
        data = await state.get_data()        
        id = data['id']        
        await state.clear()
        event =await Event.set_by_id(id=id)
        await event.update_time(date)        
        await message.answer(text=f"Время изменено на {event.date} {event.time}", reply_markup= home_eventor)
    else:
        await message.answer(text="Неверный формат", reply_markup=home_eventor)

@rt.callback_query(lambda c: c.data.startswith("rebuild:"))
async def hand_rebuild(callback: CallbackQuery, state: FSMContext):
    id = int(callback.data.split(":")[1])
    event = await Event.set_by_id(id=id)
    
    await state.set_state(RebuildEvent.id)
    await state.update_data(id = id)
    await state.set_state(RebuildEvent.new_name)

    await callback.message.answer(
        text = "Это функция позволяет изменить название, описание и время мероприятия,\
            сохраняя людей, которые следят за этим мероприятиями. \
            Если вы хотите сохранить какой-либо элемент отправьте точку.\n",
            reply_markup= home_eventor
    )
    await callback.message.edit_text(
        text = f"Текущее название мерпориятия: {event.name}. Напишите новое",        
    )    

@rt.message(RebuildEvent.new_name)
async def rebuild_name(message: Message, state: FSMContext):
    
    await state.update_data(n_name= message.text)    
    data = await state.get_data()
    await state.set_state(RebuildEvent.new_discription)
    id = int(data['id'])

    event = await Event.set_by_id(id = id)

    await message.answer(
        text=f"Напишите новое описание мероприятия \n\nТекущее описание\n{event.description}"
    )

@rt.message(RebuildEvent.new_discription)
async def rebuild_name(message: Message, state: FSMContext):
    
    await state.update_data(n_discription= message.text)    
    data = await state.get_data()
    await state.set_state(RebuildEvent.new_time)
    id = int(data['id'])

    event = await Event.set_by_id(id = id)

    await message.answer(
        text=f"Напишите новое время мероприятия \
            \n\nТекущее время:\n{event.date} {event.time}"
    )

@rt.message(RebuildEvent.new_time)
async def rebuild_name(message: Message, state: FSMContext):
    data0 = await state.get_data()
    id = int(data0['id'])
    event = await Event.set_by_id(id = id)

    date = await splitter_time(message.text)
    if date=='.': date=event.date
    if date:
        await state.update_data(n_date= message.text)    
        data = await state.get_data()
        await state.set_state(RebuildEvent.new_time)
                
        new_name= data['n_name']        
        new_description = data['n_discription']        
        
        
        if new_name=='.': new_name = event.name
        if new_description=='.': new_description = event.description
        kwarg = {
            'name': new_name,
            'date': date[0],
            'description':new_description,
            'time': date[1]
        }        
        # Обновление параметров и таблицы
        await event.update_params(event_data=kwarg)
        await event.update_db()
        n_text = f'Измение в мероприятии:\n{event.text}'
        await event.send_to_followers(text=n_text)
        n_text = f"Вот, что получилось\n\nНазвание: {event.text}\nСобщение об изменениях уже вышленно следящим"
        await message.answer(
            text=n_text,
            reply_markup=home_eventor
        )        
        await state.clear()
    else:
        await message.answer(text="Неверный формат", reply_markup=home_eventor)

# Отправка сообщений фолловерам
@rt.callback_query(lambda c: c.data.startswith("send_to_followers:"))
async def hand_rebuild(callback: CallbackQuery, state: FSMContext):
    id = int(callback.data.split(":")[1])    
    await state.set_state(MesToFolls.id.state)    
    await state.update_data(id= id)
    await state.set_state(MesToFolls.mes.state)
    await callback.message.edit_text(text="Напишите то, что вы хотитте отправить тем, кто следит за мероприятие", reply_markup=home_eventor)

@rt.message(MesToFolls.mes)
async def send_mes (message: Message, state: FSMContext):
    await state.update_data(messa = message.text)
    data0 = await state.get_data()
    id = int(data0['id'])
    event = await Event.set_by_id(id=id)
    await message.answer(text="Сообщение отправлено", reply_markup=home_eventor)
    await event.send_to_followers(text=data0['messa'])
    await state.clear()