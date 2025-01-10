from aiogram import  Router
from config import user_id_adm
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from keyboards import total_statistik, start_inl_kbs
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from db import get_row_by_condition, User

router = Router()

@router.callback_query(lambda c: c.data.startswith("home_stud:"))
async def home_page_user (callback: CallbackQuery):
    unic_code =int(callback.data.split(":")[1])
    user = User()
    await user.set_other_atributs(tg_user_id=None,unic_kod=unic_code, name=None)
    await user.say_my_name(message=callback)

@router.callback_query(lambda c: c.data.startswith("u_statistik:"))
async def statistika_stud (callback: CallbackQuery):
    unic_code =int(callback.data.split(":")[1])
    user = await get_row_by_condition(
        table="Just_users", condition_column='unic_kod',
        condition_value=unic_code
    )
    text=f"{user[2]} \nБаллы:{user[3]}\n\nИстория:{user[4]}"
    markup = start_inl_kbs(unic_code=unic_code)
    n_markup = await markup.home_stud()
    await callback.message.answer(
        text="Посмотреть топ студентов по баллам", 
        reply_markup= total_statistik
    )
    await callback.message.edit_text(
        text = text,
        reply_markup= n_markup
    )    
