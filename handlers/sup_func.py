from aiogram.types import Message, CallbackQuery
from db import (
    exists_in_db, update_user_id, get_all
)
from db import User, Starosta
from texts import studsovet_message, my_events_message, start_message
from keyboards import menu_keyboard

async def set_id_new_user(cur_user_id:int,  unic_code:int):
    for table in ["Just_users", "Starst"]:
        cor_st = False
        cor_st = await exists_in_db(
            table= table, column="unic_kod",
            value=unic_code
        )
        # Проверка на занятость ячейки
        db_user_id = await exists_in_db(
            table=table, column="tg_user_id",
            value=cur_user_id
        )        
        if cor_st==True  and db_user_id==False:
            await update_user_id(
                table=table, user_id= cur_user_id,
                unic_kod= unic_code
            )
            return True
    return False

async def chosing_role (cur_tg_id: int) -> Starosta|User:
    list_students = await get_all(
        table ="Just_users", column="tg_user_id"
    )
    if cur_tg_id in list_students:
        user = User ()
        await user.set_other_atributs(tg_user_id=cur_tg_id,unic_kod=None, name=None)
        return user
    else:
        list_starosts = await get_all(
            table ="Starst", column="tg_user_id"
        )
        if cur_tg_id in list_starosts :
            starosta = Starosta()
            await starosta.set_other_atributs(tg_user_id= cur_tg_id, unic_kod=None, name=None)
            return starosta
        return None
    
async def menu_func(mes: CallbackQuery|Message):
    tg_id = mes.from_user.id    
    markup = await menu_keyboard(
        tg_id=tg_id,
        flag = True
    )
    if isinstance(mes, CallbackQuery):        
        await mes.message.edit_text(
            text = start_message,
            reply_markup= markup
        )     

    if isinstance(mes, Message):
        await mes.answer(
            text = start_message,
            reply_markup= markup
        )