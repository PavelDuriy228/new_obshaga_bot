from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from db import get_all_if, User
from keyboards.strelki import create_strelki

async def viewer_studs(callback: CallbackQuery):
    cortege =callback.data.split(":") 
    cortege = [x for x in cortege if x!=""]    
    callback_name = cortege[0]
    # Получение кода
    unic_code = int(cortege[1])
    # Получение страницы
    index=int(cortege[2])
    # index юзера в общем списке
    page = int(cortege[3])
    # print(f"unic_code: {unic_code} \npage: {page}, \nindex: {index}")
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
    text = f"{user.name}\nБаллы:{user.count_b}\n\nИстория:\n\n{user.comment}"

    keyboard = []
    if callback_name == "my_students":
        keyboard.append([
            InlineKeyboardButton(text="⬇️Получить его ссылку", callback_data=f'stud_url:{user.unic_kod}'),    
            InlineKeyboardButton(text="🔄Очистить ячейку", callback_data=f"clear_tg_id:{user.unic_kod}")
        ])
    if callback_name == "view_studs":
        keyboard.append(
            [InlineKeyboardButton(text="Назад", callback_data=f'choise_etag')]
        )
    
    # Создание кнопок для каждого юзера
    for page2 in range(page, page+6, 2):
        if len(studnts)-1> page2:
            keyboard.append([
                # Кортедж коллбэка начало:код_старосты:текущая_страница:индекс_конкретного_юзера
                InlineKeyboardButton(text=f"{studnts[page2]}", callback_data=f'{callback_name}:{unic_code}:{page2}:{page}'),
                InlineKeyboardButton(text=f"{studnts[page2+1]}", callback_data=f'{callback_name}:{unic_code}:{page2+1}:{page}')
            ])            
        if len(studnts)-1==page2:
            keyboard.append([
                InlineKeyboardButton(text=f"{studnts[page2]}", callback_data=f'{callback_name}:{unic_code}:{page2}:{page}'),
            ])
            break
        
        
    # cd:code_strst:st_page:page_for_move
    strelki =await create_strelki(
        len_list=len(studnts),
        callback_dataU = f"{callback_name}:{unic_code}:{page}",
        page= page, range= 6
    )
    if strelki: keyboard.append(strelki)
    
    serfing = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await callback.message.edit_text(
        text=text, reply_markup=serfing,
        parse_mode="html"
    )