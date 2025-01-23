from aiogram import types, Router
import re
from config import username_bota
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from db import (
    Starosta
)
from keyboards import edit_strst, home_admin, kb_srsts
from FSMs import ForEditStName, ForDelStName
from other_func import checking_starst

router= Router()

@router.callback_query(lambda c: c.data =='edit_starst')
async def edit_starst (callback: types.CallbackQuery):
    await callback.message.edit_text(
        text = "Смена старосты подразумевает очистку ячейки от id прежнего старосты, этого старосты\
        \nУдаление же повлечет за собой полное удаление и старосты и его подопечных, однако это\
        удаление не повлечет за собой тяжких последствий т.к. бот не может изменять главную таблицу",
        reply_markup= edit_strst
    )

@router.callback_query(lambda c: c.data == 'del_strst')
async def del_strst_handl (callback: types.CallbackQuery, state: FSMContext):
    markup = await kb_srsts()    
    await state.set_state(ForDelStName.for_del_name)
    await callback.message.edit_text(
        text= "Вернуться в меню",
        reply_markup= home_admin
    )
    await callback.message.answer(
        text="Выберите старосту",
        reply_markup= markup
    )

@router.message(ForDelStName.for_del_name)
async def del_strst_handl1(message: types.Message, state:FSMContext):
    text = message.text
    await state.update_data(name = text)
    strst= Starosta()
    await strst.set_other_atributs(name=text, unic_kod=None, tg_user_id=None)
    await strst.fool_del()
    await message.answer("Староста и его подопечные удалены", reply_markup=home_admin)
    await message.answer("Вернуться обратно", reply_markup=types.ReplyKeyboardRemove())

@router.callback_query(lambda c: c.data == "replace_strst")
async def replace_id0 (callback: types.CallbackQuery, state: FSMContext):
    markup = await kb_srsts()    
    await state.set_state(ForEditStName.for_edit_name)
    await callback.message.edit_text(
        text= "Выберите старосту",
        reply_markup= home_admin
    )
    await callback.message.answer(
            text= "Если вы передумали нажмите на кнопку ниже",
            reply_markup=markup
        )

@router.message(ForEditStName.for_edit_name)
async def replace_id(message: types.Message, state: FSMContext):    
    await state.update_data(for_edit_name=message.text)
    if await checking_starst(message.text):
        await state.set_state(ForEditStName.new_name)
        await message.answer(
            text= "Теперь, напишите Фамилию и Имя нового старосты,без указания его таблицы, или нажав на кнопку ниже, сбросьте все изменения",
            reply_markup= home_admin
        )
        await message.answer(
            text="Например: \nИванов Иван", reply_markup= types.ReplyKeyboardRemove()
        )
    else:
        await message.answer(text="Неверное имя",reply_markup=home_admin)

@router.message(ForEditStName.new_name)
async def replace_id1(message: types.Message, state: FSMContext):
    await state.update_data(new_name = message.text)
    data = await state.get_data()
    old_name = data['for_edit_name']
    new_name = data['new_name']
    pattern = r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]'
    if bool(re.match(pattern, new_name)):
        starosta = Starosta()        
        await starosta.set_other_atributs(name=old_name, unic_kod=None, tg_user_id=None)
        new_name1 = f"{new_name}: {starosta.place}"
        await starosta.reset_user(new_name=new_name1)
        await message.answer("Его имя было изменено. Отправьте эту ссылку новому старосте")
        await message.answer(f"https://t.me/{username_bota}?start={starosta.unic_kod}")
    await message.answer("Вернуться в меню", reply_markup=home_admin)