import logging
from config import bot, user_id_adm

# Логгирование ошибок при отправке сообщений
async def log_error_w_sending(cur_id, error):
    error_text= f"Не удалось отправить сообщение пользователю с ID {cur_id}: {error}"
    logging.error(error_text)
    await bot.send_message(chat_id=user_id_adm, text=error_text)


async def logger_for_updating_db (text:str, error):
    error_text = f"Произошла ошибка при обновлении таблицы:{text} --- {error} "
    logging.error(error_text)
    await bot.send_message(chat_id=user_id_adm, text=error_text)