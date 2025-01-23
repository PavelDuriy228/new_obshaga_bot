from aiogram.types import Message, InputFile
from aiogram import Router
import os
from config import bot, user_id_adm

loging_router = Router()

@loging_router.message(lambda message: message.text == "/haha_logs" )
async def logging_adm (message: Message):
    # Получаем путь к текущей директории
    current_directory = os.path.dirname(__file__)
    # Формируем полный путь к файлу
    file_path = os.path.join(current_directory, 'app.log')  # Замените 'your_file.txt' на имя вашего файла
    print(file_path)
    await bot.send_document(chat_id=user_id_adm, document=InputFile(file_path), caption="Вот ваш документ!")