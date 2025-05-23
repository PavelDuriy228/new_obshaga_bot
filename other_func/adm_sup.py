from aiogram.types import Message, InlineKeyboardMarkup
from db import get_all
from config import bot, user_id_adm22, user_id_adm
from loggers.logs1 import log_error_w_sending
import re

# Проверка нового старосты по маске
async def checking_starst (text:str) -> bool:
    pattern  = r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+:\s[0-9]+этаж\(\w+(\s*\/\s*\w+)?\)$'
    return bool(re.match(pattern, text))


async def send_for_all_func (
    message: Message|None = None, markup: InlineKeyboardMarkup|None=None, 
    text: str|None = None, flag:bool = False
):
        list_tg_id = await get_all(
            table="Users", column="tg_id"
        )            
        print("Вызвана рассылка")
        for tg_id in list_tg_id:
            if tg_id and tg_id!="-1" and tg_id!=-1:                
                try:
                    if message:
                        await message.copy_to(
                            chat_id=tg_id
                        )
                        if flag:
                            await bot.send_message(
                                chat_id= tg_id, 
                                text = text,
                                reply_markup=markup,
                                parse_mode='html'
                            )
                    else:
                        await bot.send_message(
                            chat_id=tg_id,
                            text=text
                        )
                except Exception as e:
                    await log_error_w_sending(cur_id=tg_id, error=e)

# функция рассылки админам
async def send_to_adms(
    message: Message
):
    adms = (user_id_adm, user_id_adm22)
    for adm_id in adms:
        try:
            await message.copy_to(
                chat_id=adm_id
            )
        except Exception as e:
                    await log_error_w_sending(cur_id=adm_id, error=e)