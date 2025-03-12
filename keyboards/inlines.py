from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random

adm_menu_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Добавить старосту", callback_data="adm_add_starst"), 
        InlineKeyboardButton(text="Изменение старост", callback_data="edit_starst")
    ],
    [InlineKeyboardButton(text="📈Статистка", callback_data="adm_statistik")],
    [InlineKeyboardButton(text="Ссылки для старост", callback_data="stars_urls:0")]
])

edit_strst = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сменить старосту", callback_data="replace_strst")],
    [InlineKeyboardButton(text="🗑️Целиком удалить старосту", callback_data="del_strst")],
    [InlineKeyboardButton(text="🏠Домой", callback_data="adm_menu")]
])

home_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🏠Домой", callback_data="adm_menu")]
])

total_statistik = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔝Топ студентов", callback_data="full_statik:0")],
    [InlineKeyboardButton(text="Посмотреть по этажам", callback_data="choise_etag")]
])

eventor_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Создать мероприятие", callback_data="create_event")],
    [InlineKeyboardButton(text="Активные мероприятия", callback_data="active_events:0")],
    [InlineKeyboardButton(text="Все мероприятия", callback_data="all_events:0")],
    [InlineKeyboardButton(text="Поиск по названию", callback_data="search_event")]
])

# Меню для редактирования
async def GetMenuForEdit(id):    
    menu_for_edi_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отменить", callback_data=f"otmena:{id}")],
        [InlineKeyboardButton(text="Изменить время", callback_data=f"edit_time:{id}")],
        [InlineKeyboardButton(text="Пересоздание", callback_data=f"rebuild:{id}")],
        [InlineKeyboardButton(text="Сообщить следящим", callback_data=f"send_to_followers:{id}")]            
    ])
    return menu_for_edi_markup

home_eventor = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🏠Домой", callback_data="eventor_menu")]
])

mini_games= InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Шкатулка", callback_data="shkatulka"),
        InlineKeyboardButton(text="По Лапласу", callback_data="laplas")
    ]
])

async def create_shkatulki()->InlineKeyboardMarkup:
    vars = ['win_shk:0', 'win_shk:1', 'win_shk:0']
    random.shuffle(vars)
    keyboard = [
        [
            InlineKeyboardButton(text="🎁", callback_data=f"{vars[0]}"),
            InlineKeyboardButton(text="🎁", callback_data=f"{vars[1]}")
        ],
        [InlineKeyboardButton(text="🎁", callback_data=f"{vars[2]}")]
    ]    
    markup = InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
    return markup

async def etagi_inl(
    etagi:list[str],
    id_etag:list[int]
)->InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🔝Топ студентов", callback_data="full_statik:0")],
        # последний флаг 25  предназначен для простых пользователей
        [InlineKeyboardButton(text=f"{etagi[0]}", callback_data=f"view_studs:{id_etag[0]}:0:0")]
    ]
    for etag in range(1, len(etagi), 2):
        if etag+1< len(etagi):
            keyboard.append([
                InlineKeyboardButton(text=f"{etagi[etag]}", callback_data=f"view_studs:{id_etag[etag]}:0:0"),
                InlineKeyboardButton(text=f"{etagi[etag+1]}", callback_data=f"view_studs:{id_etag[etag+1]}:0:0")
            ])
        else:
            keyboard.append(
                [InlineKeyboardButton(text=f"{etagi[etag]}", callback_data=f"view_studs:{id_etag[etag]}:0:0")]
            )
    markup = InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
    return markup