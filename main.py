from typing import Any
from aiogram import types
import logging
import asyncio
import traceback
from config import dp, bot, user_id_adm, scheduler
# Роутеры 
from handlers import *
from db import reader_gs, actualitic_status3, reader_old_table
from logging_hand import loging_router

# Включение ввсех роутеров
routers = [
    gen_router, gen_adm_router, edit_strst_routers, gen_star_router, star_router2,
    statistik_router, gen_user_router, loging_router, gen_event_rt, funcs_event_rt,
    events_rt, event_user_router, gen_router2, proba_router
]

for cur_router in routers:
    dp.include_router(cur_router)

async def main(message: types.Message = None):
    try:
        # Благодаря этому в консоли появлятся вся информации о работе тг бота
        logging.basicConfig(level=logging.INFO)
        # Настройка конфигурации логирования
        
#________ Логгирование в спец файл
        # logging.basicConfig(
        #     filename='app.log',  # Имя файла для записи логов
        #     level=logging.DEBUG,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        #     format='%(asctime)s - %(levelname)s - %(message)s'  # Формат сообщений
        # )
        # Назначение выполнение функции чтения данных с таблицы        
        scheduler.add_job(reader_gs, 'cron', hour=3, minute =20)
        scheduler.add_job(reader_old_table, 'cron', hour=3, minute =20)
        # потестить
        scheduler.add_job(actualitic_status3, 'interval', minutes = 30)
        scheduler.start()
        if scheduler:
            print ("---Задача назначена")

        #logging.info("____Бот начал работу___")
        # Этим мы опрашиваем тг на наличие уведомлений
        await dp.start_polling(bot)
        
    except Exception as e:
        # Получаем строку с информацией об ошибке
        error_message = traceback.format_exc()
        if message:
            await bot.send_message(chat_id=user_id_adm, text="Произошла ошибка:")
            await bot.send_message(chat_id=user_id_adm, text=error_message)
        else:
            logging.error(f"Произошла ошибка: {error_message}")

# Запуск ассинхронной функции main
if __name__ == "__main__":
    asyncio.run(main())