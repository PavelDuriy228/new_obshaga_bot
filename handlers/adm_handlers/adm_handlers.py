from aiogram import types, Router
from config import username_bota
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from db import (
    create_code, create_new_user, get_all
)
from keyboards import adm_menu_markup, home_admin, total_statistik
from FSMs import StateName
from other_func import checking_starst
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

router = Router()

@router.callback_query(lambda c: c.data == "adm_menu")
async def adm_menu(call_qu: CallbackQuery, state: FSMContext):
    await state.clear()
    await call_qu.message.edit_text(
        "Меню кнопок админа", reply_markup= adm_menu_markup
    )


@router.callback_query(lambda c: c.data.startswith('adm_add_starst'))
async def add_new_starst0(callback_query: CallbackQuery, state:FSMContext):
    await state.set_state(StateName.name_st)
    await callback_query.message.edit_text(
        "Напшите ФИО или ФИ старосты и название его таблицы.\nНапример:\nИванов Иван: 3этаж(п/к)"        
    )    

@router.message(StateName.name_st)
async def add_new_starst1 (message: Message, state: FSMContext):
    text = message.text
    if await checking_starst(text=text):
        await state.update_data(name = text)
        code = await create_code(
            table="Starst", start=500_001,
            end=1_000_000
        )
        await create_new_user(
            code=code, table="Starst", place=text.split(":")[1],
            name = text
        )
        await message.answer(
            "Ниже будет ссылка для вашего старосты. Перейдя по ней он автоматически авторизуется в системе",
            reply_markup= home_admin
        )
        await message.answer(f"https://t.me/{username_bota}?start={code}")
        await state.clear()
    
    else: 
        await message.answer("Что то не так, попробуйте ещё раз",reply_markup= home_admin)

@router.callback_query(lambda c: c.data == "adm_statistik")
async def statistika_adm (callback : CallbackQuery):
    starosts = await get_all(
        table='Starst', column="name"
    )
    text= 'Все старосты:\n\n'
    i=1
    for item in starosts:
        text+= f"{i}. {item}\n"
        i+=1
    await callback.message.edit_text(
        text = text,
        reply_markup=home_admin
    )
    await callback.message.answer(
        text = "Нажмите на кнопку ниже, чтобы посмотреть топ студентов по баллам",
        reply_markup=total_statistik
    )

@router.callback_query(lambda c: c.data.startswith("stars_urls:"))
async def links_stars (callback : CallbackQuery):
    page =int( callback.data.split(":")[1] )
    names = await get_all(
        table='Starst', column="name"
    )
    codes = await get_all(
        table='Starst', column="unic_kod"
    )
    text = f"Ссылка для {names[page]}: \n\n https://t.me/{username_bota}?start={codes[page]}"

    keyboard = []
    keyboard.append([InlineKeyboardButton(text="Домой", callback_data="adm_menu")])
    # только вперед
    if page-1 <0 and page+1 < len(names):
        keyboard.append([
            InlineKeyboardButton(text="➡️", callback_data=f"stars_urls:{page+1}")    
        ])
    # только назад
    if page -1>=0 and page +1 >= len (names):
        keyboard.append([
            InlineKeyboardButton(text="⬅️", callback_data=f"stars_urls:{page-1}")
        ])
    if page - 1 >= 0 and page +1<len(names):
        keyboard.append([
            InlineKeyboardButton(text="⬅️", callback_data=f"stars_urls:{page-1}"),
            InlineKeyboardButton(text="➡️", callback_data=f"stars_urls:{page+1}")
        ])
    
    serfing = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.edit_text(
        text=text,
        reply_markup= serfing
    )