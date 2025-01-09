from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

adm_menu_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Добавить старосту", callback_data="adm_add_starst"), 
        InlineKeyboardButton(text="Изменение старост", callback_data="edit_starst")
    ],
    [InlineKeyboardButton(text="📈Статистка", callback_data="adm_statistik")]
])

edit_strst = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сменить старосту", callback_data="replace_strst")],
    [InlineKeyboardButton(text="Целиком удалить старосту", callback_data="del_strst")],
    [InlineKeyboardButton(text="Домой", callback_data="adm_menu")]
])

home_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Домой", callback_data="adm_menu")]
])
