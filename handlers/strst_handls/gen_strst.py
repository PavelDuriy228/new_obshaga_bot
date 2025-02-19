from aiogram import Router
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from db import (
    User, get_all_if
)
from keyboards import start_inl_kbs
from keyboards.strelki import create_strelki
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from other_func.viewer_studs import viewer_studs

router = Router()

@router.callback_query(lambda c: c.data.startswith("star_home_page:"))
async def star_home_page (callback: CallbackQuery, state: FSMContext):
    await state.clear()
    unic_code = callback.data[14:]
    
    inlens = start_inl_kbs(unic_code=unic_code)
    mrk = await inlens.star_markup()
    await callback.message.edit_text(
        text="Выберите действие",
        reply_markup= mrk
    )

@router.callback_query(lambda c: c.data.startswith("my_students:"))
async def star_students (callback: CallbackQuery):    
    await viewer_studs(
        callback=callback
    )
    

