from aiogram import types, Router
from config import username_bota
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from db import (
    create_code, create_new_user
)
from keyboards import adm_menu_markup
from FSMs import StateName
from other_func import checking_starst

router = Router()

@router.callback_query(lambda c: c.data == "adm_menu")
async def adm_menu(call_qu: types.CallbackQuery, state: FSMContext):
    state.clear()
    await call_qu.message.edit_text(
        "Меню кнопок админа", reply_markup= adm_menu_markup
    )


@router.callback_query(lambda c: c.data.startswith('adm_add_starst'))
async def add_new_starst0(callback_query: types.CallbackQuery, state:FSMContext):
    await state.set_state(StateName.name_st)
    await callback_query.message.edit_text(
        "Напшите ФИО или ФИ старосты и название его таблицы.\nНапример:\nИванов Иван: 3этаж(п/к)"        
    )    

@router.message(StateName.name_st)
async def add_new_starst1 (message: types.Message, state: FSMContext):
    text = message.text
    if await checking_starst(text=text):
        await state.update_data(name = text)
        code = await create_code(
            table="Starst", start=500_001,
            end=1_000_000
        )
        await create_new_user(
            code=code, table="Starst", place=text.split(":")[1],
            name = text.split(":")[0]
        )
        await message.answer(
            "Ниже будет ссылка для вашего старосты. Перейдя по ней он автоматически авторизуется в системе"            
        )
        await message.answer(f"https://t.me/{username_bota}?start={code}")
        await state.clear()
    
    else: 
        await message.answer("Что то не так, попробуйте ещё раз")