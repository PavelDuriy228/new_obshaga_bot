from aiogram import types, Router
from config import username_bota
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from db import (
    update_value
)
from keyboards import start_inl_kbs, home_admin
from FSMs import StateName
from other_func import checking_starst
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data.startswith("stud_url:"))
async def star_home_page (callback: CallbackQuery):    
    unic_code = callback.data[8:]
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