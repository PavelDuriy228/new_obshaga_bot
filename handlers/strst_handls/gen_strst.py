from aiogram import Router
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from db import (
    User, get_all_if, Starosta
)
from keyboards import start_inl_kbs, home_admin
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

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
    cortege =callback.data.split(":") 
    cortege = [x for x in cortege if x!=""]
    print(cortege)
    # Получение кода
    unic_code = int(cortege[1])
    # Получение страницы
    page=int(cortege[2])
    # index юзера в общем списке
    index = int(cortege[3])
    print(f"unic_code: {unic_code} \npage: {page}, \nindex: {index}")
    # Список всех студентов старосты
    studnts = await get_all_if(
        table="Just_users",
        column="name", condition_column="unic_kod_strtsi",
        condition_value=unic_code
    )    
    
    user = User()    
    await user.set_other_atributs(
        unic_kod=None, name=studnts[index],
        tg_user_id=None
    )
    text = f"{user.name}\nБаллы:{user.count_b}\n\nИстория:{user.comment}"

    keyboard = []    
    keyboard.append([
        InlineKeyboardButton(text="Получить его ссылку", callback_data=f'stud_url:{user.unic_kod}'),    
        InlineKeyboardButton(text="Очистить ячейку", callback_data=f"clear_tg_id:{user.unic_kod}")
    ])
    
    for page2 in range(page, page+6, 2):
        if len(studnts)-1> page2:
            keyboard.append([
                # Кортедж коллбэка начало:код_старосты:текущая_страница:индекс_конкретного_юзера
                InlineKeyboardButton(text=f"{studnts[page2]}", callback_data=f'my_students:{unic_code}:{page}:{page2}'),
                InlineKeyboardButton(text=f"{studnts[page2+1]}", callback_data=f'my_students:{unic_code}:{page}:{page2+1}')
            ])            
        if len(studnts)-1==page2:
            keyboard.append([
                InlineKeyboardButton(text=f"{studnts[page2]}", callback_data=f'my_students:{unic_code}:{page}:{page2}'),
            ])
            break
        
    action = 0
    nazad = page-4 
    if nazad<0:
        nazad =0
        keyboard.append([
            InlineKeyboardButton(text="➡️", callback_data=f"my_students:{unic_code}:{page+4}:{page}")    
        ])
        action = 1
    vper = page +4
    if vper > len(studnts):
        vper = page
        keyboard.append([
            InlineKeyboardButton(text="⬅️", callback_data=f"my_students:{unic_code}:{page-4}:{page}")
        ])
        action = 1

    #print(f"Назад:{nazad}\nВперед{vper}")
    if action == 0:
        keyboard.append([
            InlineKeyboardButton(text="⬅️", callback_data=f"my_students:{unic_code}:{nazad}:{page}"),
            InlineKeyboardButton(text="➡️", callback_data=f"my_students:{unic_code}:{vper}:{page}")        
        ])
    serfing = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await callback.message.edit_text(text=text, reply_markup=serfing)

