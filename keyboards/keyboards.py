from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import get_all

async def kb_srsts ():
    starosts = await get_all(
        table="Starst",
        column="name"
    )
    if len(starosts)==0:
        return ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = []
    for st in starosts:        
        keyboard.append([KeyboardButton(text=f"{st}")])

    markup = ReplyKeyboardMarkup(
        keyboard= keyboard,
        resize_keyboard=True
    )           
    return markup