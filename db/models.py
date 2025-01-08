import aiosqlite
from db import (
    get_row_by_condition, delete_from_db,
    update_value, get_all_if
)
from keyboards import start_inl_kbs
from aiogram.types import Message

#     unic_kod INT,
#     tg_user_id INT,
#     name TEXT,
#     count_b INT,
#     comment MEDIUMTEXT,
#     unic_kod_strtsi INT
class BaseUser():
    def __init__(self, unic_kod: int=-1, tg_user_id: int=-1, name: str=""):
        self.unic_kod = unic_kod
        self.tg_user_id = tg_user_id
        self.name = name
        if self.__class__.__name__ == "User": self.table = "Just_users"
        if self.__class__.__name__ == "Starosta": self.table = "Starst"
    
    async def get_atributs (self, unic_kod: int|None, name: str| None, tg_user_id: int|None ):
        params ={
            "unic_kod": unic_kod,
            "tg_user_id": tg_user_id, 
            "name": name
        }
        for key, item in params.items() :
            if key != None:                 
                user =await get_row_by_condition(
                    table=self.table,
                    condition_column=f"{key}",
                    condition_value= item
                )    
                return user

    #             
    async def say_my_name (self, message: Message):
        cur_name = self.name
        text = f"Здравствуйте,{cur_name}. \nВот меню действий:"
        inl_kb = start_inl_kbs()
        # для простого юзера
        if self.table == "User":     cur_markup = inl_kb.user_markup()
        # Для старосты
        if self.table == "Starosta": cur_markup = inl_kb.star_markup()
        
        await message.answer(
            text=text,
            reply_markup=cur_markup
        )
    # Функция полного удаления какого-либо пользователя
    async def del_me(self):
        await delete_from_db(
            table=self.table,
            condition_column="unic_kod",
            condition_value=self.unic_kod
        )
    # Функция очистки tg_id
    async def clear_tg_id (self):
        await update_value(
            table = "Starst", column="tg_user_id",
            value=-1, condition_column="unic_kod",
            condition_value=self.unic_kod
        )
    

# класс для студента        
class User(BaseUser):
    def __init__(
            self, unic_kod: int=-1, tg_user_id: int=-1, name: str="",
            count_b: int=-1, comment: str="", unic_kod_strtsi: int=-1
     ):
        self.unic_kod = unic_kod    
        self.tg_user_id = tg_user_id
        self.name = name                                                                                                                    
        self.count_b = count_b
        self.comment= comment
        self.unic_kod_strtsi = unic_kod_strtsi
        
    @classmethod        
    async def set_other_atributs (cls, unic_kod: int|None, name: str| None, tg_user_id: int|None ):
        user = await BaseUser.get_atributs(
            unic_kod=unic_kod,
            name= name, tg_user_id=tg_user_id
        )
        return cls(
            user[0], user[1], user[2],
            user[3], user[4], user[5]
        )

    async def set_comment (self, new_com: str):
        await update_value(
            table="Just_users", column="comment",
            value=new_com, condition_column="unic_kod",
            condition_value=self.unic_kod
        )
    async def set_bals (self, new_bals: str):
        await update_value(
            table="Just_users", column="count_b",
            value=new_bals, condition_column="unic_kod",
            condition_value=self.unic_kod
        )
    async def just_update_value(self, new_value, column:str):
        await update_value(
            table="Just_users", column=column,
            value=new_value, condition_column="unic_kod",
            condition_value=self.unic_kod
        )

    # unic_kod INT,
    # tg_user_id INT,
    # name TEXT,
    # place TEXT 
class Starosta(BaseUser):
    def __init__(self, unic_kod: int=-1, tg_user_id: int=-1, name: str="", place:str=""):
        self.unic_kod = unic_kod
        self.tg_user_id = tg_user_id
        self.name = name
        self.place = place        

    @classmethod        
    async def set_other_atributs (cls, unic_kod: int|None, name: str| None, tg_user_id: int|None ):
        user = await BaseUser.get_atributs(
            unic_kod=unic_kod,
            name= name, tg_user_id=tg_user_id
        )
        return cls(
            user[0], user[1], 
            user[2], user[3]
        )
    
    async def my_students (self):
        my_students = await get_all_if(
            table = "Just_users", column= "name",
            condition_column="unic_kod_strtsi",
            condition_value=self.unic_kod
        )
    async def fool_del(self):
        await delete_from_db(
            table="Just_users",
            condition_column="unic_kod_strtsi",
            condition_value=self.unic_kod
        )
        await self.del_me()
