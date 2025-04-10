from aiogram import Router
from config import username_bota
from db import (
    update_value, get_rows_by_condition,
    get_all_if
)
from keyboards import  start_inl_kbs
from other_func import sort_list0
from aiogram.types import  CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data.startswith("stud_url:"))
async def star_home_page (callback: CallbackQuery):    
    unic_code = callback.data.split(":")[1]
    await callback.message.answer(f"https://t.me/{username_bota}?start={unic_code}")

@router.callback_query(lambda c: c.data.startswith("clear_tg_id:"))
async def star_home_page (callback: CallbackQuery):    
    unic_code = callback.data.split(":")[1]
    await update_value(
        table="Just_users", column="tg_user_id",
        value=-1, condition_column="unic_kod",
        condition_value=unic_code    
    )
    await callback.message.answer(f"Теперь этот студент не сможет пользоваться ботом. Отправьте эту ссылку новому пользоваелю")
    await callback.message.answer(f"https://t.me/{username_bota}?start={unic_code}")

@router.callback_query(lambda c: c.data.startswith("st_statistik:"))
async def star_statistika (callback: CallbackQuery):    
    unic_code = callback.data.split(":")[1]
    users = await get_rows_by_condition(
        table="Just_users", condition_column="unic_kod_strtsi",
        condition_value=unic_code
    )
    #print(f'\nusers\n{users}\n')
    text = await sort_list0(users=users)
    markup = start_inl_kbs(unic_code=unic_code)    
    n_markup = await markup.home_star()
    await callback.message.edit_text(
        text = text,
        reply_markup=n_markup,
        parse_mode="html"
    )
    # await callback.message.answer(
    #     text="Нажмите, чтобы посмотреть полную статистику",
    #     reply_markup=total_statistik
    # )

@router.callback_query(lambda c: c.data.startswith("urls_my_studs:"))
async def star_statistika (callback: CallbackQuery):    
    unic_code = callback.data.split(":")[1]
    names = await get_all_if(
        table="Just_users", column="name",
        condition_column="unic_kod_strtsi",
        condition_value=unic_code
    )
    codes = await get_all_if(
        table="Just_users", column="unic_kod",
        condition_column="unic_kod_strtsi",
        condition_value=unic_code
    )
    for i in range(len(names)):
        await callback.message.answer(
            text=f"Ссылка для: \n{names[i]}\n\nhttps://t.me/{username_bota}?start={codes[i]}"
        )
    