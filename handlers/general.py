from aiogram import types, Router
from config import user_id_adm
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from db import (
    exists_in_db
)
from .sup_func import set_id_new_user, chosing_role
from keyboards import adm_menu_markup

router = Router()

@router.message(CommandStart())
async def h_start (message:types.Message, state:FSMContext, command: CommandStart):
    # Получение кода при старте бота
    unic_code = command.args
    cur_user_id = message.from_user.id
    # Очистка всех Машин состояний
    await state.clear()
    await message.answer("Этот бот создан для учета баллов в общежитии", reply_markup= types.ReplyKeyboardRemove())

    if not ( unic_code  is None ):
        # Перевод в int command.args
        await message.answer(unic_code)
        unic_code = int(unic_code)
        # Проверка на существование кода в БД
        nalich = await set_id_new_user(
            cur_user_id=cur_user_id, 
            unic_code=unic_code
        )
        if nalich: await message.answer("Ваш id добавлен в БД. Теперь вам не нужна специальная ссылка")
        else: await message.answer("Неверный код старта")
    
    cur_user = await chosing_role(cur_tg_id=cur_user_id)
    if not (cur_user is None):
        # Приветственное сообщение с менюшкой
        cur_user.say_my_name(message=message)
    if cur_user_id == user_id_adm:
        await message.answer("Здравствуйте, администратор", reply_markup=adm_menu_markup)