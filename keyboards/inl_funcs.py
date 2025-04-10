from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup

async def menu_keyboard(tg_id:int, flag: bool = False) -> list[InlineKeyboardButton]:
    keyboard = [
        [InlineKeyboardButton(text="Мои мероприятия", callback_data=f"start_event:{tg_id}")],
        [InlineKeyboardButton(text="Посмотреть по этажам", callback_data="choise_etag")],
        [InlineKeyboardButton(text="Студсовет", callback_data=f"studsovet:0:0")],    
    ]
    if flag:
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    return  keyboard