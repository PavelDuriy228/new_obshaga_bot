from db import (
    get_row_by_condition, 
    execute_write_query, get_value_by_condition,
    update_value, create_code
)
from config import bot
from loggers.logs1 import log_error_w_sending
from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup, Message
from other_func import actualitic_date, send_for_all_func
  

class Event ():
    def __init__(self, name, date, description,time, id: int = 0, joined_users_id: str=None, joined_users_username: str=None, status: str=None):
        self.name = name
        self.description = description
        self.date = date        
        self.time = time
        self.text = f"Мероприятие: \n{self.name}\n\n{self.description}\nКогда: {self.date} в {self.time}"
        self.id = id
        self.joined_users_id = joined_users_id
        self.joined_users_username = joined_users_username
        self.status = status

    @classmethod
    async def setting (cls, name, time,description, date):
        event = cls(name, date, description, time)        
        return event
    
    async def send_for_all (self, message: Message):
        event_joining =InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Участвовать", callback_data=f"join:{self.id}")] ##
        ]) 

        await send_for_all_func(
            message=message,
            markup=event_joining,
            flag=True,
            text=f"🎉 Новое мероприятие!📅 Название: <b>{self.name}</b>\n🕒 Время: {self.date} {self.time}\nНе упусти возможность присоединиться! Если ты хочешь получать уведомления об этом мероприятии, нажми на кнопку ниже:",                        
        )
            
    
    async def send_to_followers(self,text: str):   
        print(self.joined_users_id)
        if self.joined_users_id:
            list_f =  self.joined_users_id.split(" ")
            list_f = [x for x in list_f if x!=""]
        if list_f:
            for cur_id in list_f:
                try:
                    cur_id.strip()
                    if cur_id != "None": await bot.send_message(                        
                        chat_id=int(cur_id), text= text,
                        parse_mode="html"
                    )
                except Exception as e:
                    await log_error_w_sending(cur_id=cur_id, error=e)

    async def add_to_table(self):
        code = await create_code(
            table="Events", start=1_000_000,
            end=1_500_000
        )        
        self.status = await actualitic_date(f"{self.date} {self.time}")
        query = f"INSERT INTO Events (unic_kod, event_name, even_desription, event_date, event_time, status) VALUES (?, ?, ?, ?, ?, ?)"
        await execute_write_query(query, (code, self.name, self.description, self.date, self.time, self.status))
        self.id = await get_value_by_condition(
            table="Events", column="unic_kod",
            condition_value= self.name,
            condition_column="event_name"
        )   

    @classmethod
    async def set_w_name(cls, name):
        row = await get_row_by_condition(
            table="Events", condition_column="event_name",
            condition_value= name
        )
        if row:
            event = cls(
                row[1], row[3], row[2], row[4], row[0], row[5], row[6], row[7]
            )
            return event
    
    @classmethod
    async def set_by_id(cls, id):
        row = await get_row_by_condition(
            table="Events", condition_column="unic_kod",
            condition_value= id
        )
        if row:
            event = cls(
                row[1], row[3], row[2], row[4], row[0], row[5], row[6], row[7]
            )
            return event  
        
    async def diactivate(self):
        self.status = "NonActive"
        await update_value(
            table='Events', column="status",
            value=self.status, condition_column="unic_kod",
            condition_value=self.id
        )
        await self.send_to_followers(
            text=f"Мероприприяте: {self.name} -- отменено"
        )
    
    async def update_time(self, new_time: list):        
        self.status = await actualitic_date(date1=f"{new_time[0]} {new_time[1]}")
        # Изменение даты
        await update_value(
            table="Events", condition_column ='unic_kod',
            condition_value=self.id,  column="event_date",
            value= new_time[0]
        )
        # Изменение времени
        await update_value(
            table="Events", condition_column ='unic_kod',
            condition_value=self.id,  column="event_time",
            value= new_time[1]
        )
    async def update_params (self, event_data: dict):
        self.name = event_data.get('name', self.name)
        self.date = event_data.get('date', self.date)
        self.description = event_data.get('description', self.description)
        self.time = event_data.get('time', self.time)   

        # Установка актуального статуса
        self.status = await actualitic_date(date1=f"{self.date} {self.time}")     
        await self.set_text()
        
    async def update_db (self, param: int=0):
        # Обновление в таблице базовых параметров
        if param ==0:
            set_values = [self.name, self.description, self.date, self.time, self.status]
            columns = ['event_name', 'even_desription', 'event_date', 'event_time', 'status']
        # Обновление в бд данных для отправки пользователям сообщений
        if param == 1:
            set_values = [self.joined_users_id, self.joined_users_username]
            columns = ['joined_users_id', 'joined_users_username']
        for i in range(len(columns)):
            await update_value(
                table='Events', 
                column=columns[i], value=set_values[i],
                condition_column='unic_kod', condition_value=self.id
            )
    async def set_text (self):
        self.text = f"Мероприятие: \n{self.name}\n\n{self.description}\nКогда:{self.date} в {self.time}"    