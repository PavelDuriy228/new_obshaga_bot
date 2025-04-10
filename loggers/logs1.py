import logging
from config import bot, user_id_adm

blocked_eror = "Telegram server says - Forbidden: bot was blocked by the user"

async def send_to_admin(text:str):
    logging.error(text)
    await bot.send_message(chat_id=user_id_adm, text=text)

# Логгирование ошибок при отправке сообщений
async def log_error_w_sending(cur_id, error):
    error_text= f"------------- Не удалось отправить сообщение пользователю с ID {cur_id}: {error}"
    if error!= blocked_eror:
        await send_to_admin(text= error_text)    


async def logger_for_updating_db (text:str, error):
    error_text = f"------------- Произошла ошибка при обновлении таблицы:{text} --- {error} "
    await send_to_admin (text=error_text)    