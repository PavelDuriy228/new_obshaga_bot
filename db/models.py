import aiosqlite
from db import (
    execute_select_query, get_row_by_condition, delete_from_db,
    update_value    
)

#     unic_kod INT,
#     tg_user_id INT,
#     name TEXT,
#     count_b INT,
#     comment MEDIUMTEXT,
#     unic_kod_strtsi INT

class User:
    tg_user_id = -1, count_b = -1 ,comment = "", unic_kod_strtsi = -1
    unic_kod = -1, name = -1
    def __init__(
            self, unic_kod: int|None, tg_user_id: int|None, name: str| None,
            count_b: int, comment: str, unic_kod_strtsi: int
     ):
        self.unic_kod = unic_kod    
        self.tg_user_id = tg_user_id
        self.name = name                                                                                                                    
        self.count_b = count_b
        self.comment= comment
        self.unic_kod_strtsi = unic_kod_strtsi

    @classmethod        
    async def set_other_atributs (cls, unic_kod: int|None, name: str| None, tg_user_id: int|None ):
        params ={
            "unic_kod": unic_kod,
            "tg_user_id": tg_user_id, 
            "name": name
        }
        for key, item in params.items() :
            if key != None:                 
                user =await get_row_by_condition(
                    table="Just_users",
                    condition_column=f"{key}",
                    condition_value= item
                )    
                return cls(
                    user[0], user[1], user[2],
                    user[3], user[4], user[5]
                )

    async def del_me(self):
        await delete_from_db(
            table="Just_users",
            condition_column="unic_kod",
            condition_value=self.unic_kod
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

class Post:
    def __init__(self, post_id: int, user_id: int, content: str):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content

    async def save(self):
        query = "INSERT INTO posts (user_id, content) VALUES (?, ?)"
        params = (self.user_id, self.content)
        await execute_select_query(query, params)

    @classmethod
    async def get_by_id(cls, post_id: int):
        query = "SELECT * FROM posts WHERE id = ?"
        params = (post_id,)
        result = await execute_select_query(query, params)
        if result:
            return cls(*result[0])  # Предполагается, что результат содержит все поля
