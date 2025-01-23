from aiogram import  Router
from db import (
    get_rows_for_statik
)
from other_func import sort_list0
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

router= Router ()

@router.callback_query(lambda c: c.data.startswith ("full_statik:"))
async def statistika (callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    # Получение всех студентов в виде списка в списке
    users = await get_rows_for_statik()
    # Использование фуникции сортировки массива
    text = await sort_list0(users=users)
    # Разбитие текста по строкам
    splited_text = text.splitlines()
    line_count = len(splited_text)
    new_text = ""
    keyboard = []
    for indx in range(page, page+50):
        if indx >= line_count: break
        new_text+=f"{splited_text[indx]}\n"
    
    # Если есть возможность двигаться тольок назад
    if page+50 >=line_count and page-50 >= 0:
        keyboard.append([
            InlineKeyboardButton(text="⬅️", callback_data=f"full_statik:{page-50}")    
        ])
    # Если есть возможность двигаться только вперед        
    if page + 50 <line_count and page - 50 <0:
        keyboard.append([
            InlineKeyboardButton(text="➡️", callback_data=f"full_statik:{page+50}")    
        ])
    # Если есть возможность двигаться вправо и влево
    if page + 50 <line_count and page - 50 >=0:
        keyboard.append([
            InlineKeyboardButton(text="➡️", callback_data=f"full_statik:{page+50}"),
            InlineKeyboardButton(text="⬅️", callback_data=f"full_statik:{page-50}")
        ])
    serfing = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await callback.message.edit_text(
        text=new_text, reply_markup= serfing
    )
    