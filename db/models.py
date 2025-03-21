from db import (
    get_row_by_condition, delete_from_db,
    update_value, get_all_if, create_code, create_new_user2
)
from keyboards import start_inl_kbs
from aiogram.types import Message, CallbackQuery

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
    
    async def get_atributs (self, unic_kod: int|None, name: str| None, tg_user_id: int|None ):
        params ={
            "unic_kod": unic_kod,
            "tg_user_id": tg_user_id, 
            "name": name
        }
        if self.__class__.__name__ == "User": self.table = "Just_users"
        if self.__class__.__name__ == "Starosta": self.table = "Starst"
        for key, item in params.items() :
            # print(f"key{key}, item:{item}")
            if item != None:                 
                user =await get_row_by_condition(
                    table=self.table,
                    condition_column=f"{key}",
                    condition_value= item
                )                    
                return user
        return None

    #             
    async def say_my_name (self, message: Message| CallbackQuery):
        cur_name = self.name
        text = f"Здравствуйте, {cur_name}. \nВот меню действий:"
        inl_kb = start_inl_kbs(unic_code=self.unic_kod)
        # для простого юзера
        if self.table == "Just_users":     
            cur_markup = await inl_kb.user_markup()
            text = f"Здравствуйте, {cur_name}, у вас {self.count_b} баллов. \nВот меню действий:"
        # Для старосты
        if self.table == "Starst": cur_markup = await inl_kb.star_markup()
        
        if isinstance(message, Message):
            await message.answer(
                text=text,
                reply_markup=cur_markup
            )
        if isinstance(message, CallbackQuery):
            await message.message.edit_text(
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
    async def reset_user(self, new_name):
        await self.clear_tg_id()
        await update_value(
            table = "Starst", column="name",
            value=new_name, condition_column="unic_kod",
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
            
    async def set_other_atributs (self, unic_kod: int|None, name: str| None, tg_user_id: int|None ):
        user = await self.get_atributs(
            unic_kod=unic_kod,
            name= name, tg_user_id=tg_user_id
        )
        if  user is None:
            user = [-1, -1, "", -1, "", -1]
        return self.__init__(
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
    async def register_user(self, name:str, count_b: int, comment: str, unic_c_stars:int):
        cod =await create_code(
            table= "Just_users", start=1, end=499_999
        )
        return self.__init__(
            unic_kod=cod, tg_user_id=-1, name=name,
            count_b=count_b, comment=comment,
            unic_kod_strtsi=unic_c_stars
        )
    async def add_to_db (self):
        await create_new_user2(
            code=self.unic_kod, name = self.name,
            count_b=self.count_b, 
            comment=self.comment,
            unic_kod_strtsi=self.unic_kod_strtsi
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

     
    async def set_other_atributs (self, unic_kod: int|None, name: str| None, tg_user_id: int|None ):
        #instance = self(unic_kod=unic_kod, name=name, tg_user_id=tg_user_id)

        user = await self.get_atributs(            
            unic_kod=unic_kod,
            name= name, 
            tg_user_id=tg_user_id
        )
        # print(self.table)
        # print(user)
        return self.__init__(
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
