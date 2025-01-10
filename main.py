from typing import Any
from aiogram import types
from aiogram.filters import CommandStart
import logging
import asyncio
import traceback
from config import dp, bot, user_id_adm
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# Роутеры 
from handlers import *

# Включение ввсех роутеров
dp.include_router(gen_router)
dp.include_router(gen_adm_router)
dp.include_router(edit_strst_routers)
dp.include_router(gen_star_router)
dp.include_router(star_router2)
dp.include_router(statistik_router)
dp.include_router(gen_user_router)

async def main(message: types.Message = None):
    try:
        # Благодаря этому в консоли появлятся вся информации о работе тг бота
        logging.basicConfig(level=logging.INFO)
        # Назначение выполнение функции чтения данных с таблицы
        # scheduler = AsyncIOScheduler()
        # scheduler.add_job(reader, 'cron', hour=23, minute =30)
        # scheduler.start()
        # if scheduler:
        #     print ("---Задача назначена")

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