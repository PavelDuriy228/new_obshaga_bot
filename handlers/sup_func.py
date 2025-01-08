from db import (
    exists_in_db, update_user_id, get_all
)
from db import User, Starosta
from aiogram.types import Message

async def set_id_new_user(cur_user_id:int,  unic_code:int):
    for table in ["Just_users", "Starst"]:
        cor_st = False
        cor_st = await exists_in_db(
            table= "Just_users", column="unic_kod",
            value=unic_code
        )
        if cor_st :
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
        user = await User.set_other_atributs(tg_user_id=cur_tg_id)
        return user
    else:
        list_starosts = await get_all(
            table ="Just_users", column="tg_user_id"
        )
        if cur_tg_id in list_starosts :
            starosta = await Starosta.set_other_atributs(tg_user_id= cur_tg_id)
            return starosta
        return None