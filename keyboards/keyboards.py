from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import get_all

async def kb_srsts ():
    starosts = await get_all(
        table="Starst",
        column="name"
    )
    keyboard = []
    for i in range(len(starosts)):
        st_in_button = f"{starosts[i]}"
        keyboard.append([KeyboardButton(text=f"{st_in_button}")])

    markup = ReplyKeyboardMarkup(
        keyboard= keyboard,
        resize_keyboard=True
    )           
    return markup