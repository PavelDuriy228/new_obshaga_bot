from aiogram import types, Router
from config import user_id_adm, user_id_eventor, user_id_adm2
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from .sup_func import set_id_new_user, chosing_role, menu_func
from keyboards import adm_menu_markup, eventor_markup, mini_games
from db import reader_gs, get_all, create_new_user3
from texts import  fedback_message

router = Router()

@router.message(CommandStart())
async def h_start (message:types.Message, state:FSMContext, command: CommandStart):
    # Получение кода при старте бота
    unic_code = command.args
    cur_user_id = message.from_user.id
    # Очистка всех Машин состояний
    await state.clear()
    await message.answer(
        text = fedback_message
    )

    await menu_func(
        mes= message
    )    
    
    if unic_code  :
        # Перевод в int command.args
        unic_code = int(unic_code)
        # Проверка на существование кода в БД
        nalich = await set_id_new_user(
            cur_user_id=cur_user_id, 
            unic_code=unic_code
        )
        print(nalich)
        if nalich: await message.answer("Ваш id добавлен в БД. Теперь вам не нужна специальная ссылка")
        else: await message.answer("Неверный код старта")
    
    cur_user = await chosing_role(cur_tg_id=cur_user_id)
    
    list_tg_id = await get_all(
        table='Users', column='tg_id'
    )


    if cur_user_id not in list_tg_id:
        print(
            "Этого пользователя нет в базе"
        )
        await create_new_user3(
            tg_id=cur_user_id,
            tg_username= message.from_user.username
        )
    
        
    if cur_user is not None:
        # Приветственное сообщение с менюшкой
        await cur_user.say_my_name(message=message)
    
    if str(cur_user_id) == user_id_adm or  message.from_user.username == user_id_adm2:
        await message.answer("Здравствуйте, администратор", reply_markup=adm_menu_markup)

    if str(cur_user_id) == user_id_eventor:        
        await message.answer(text="Здравствуйте, создатель мероприятий", reply_markup= eventor_markup)

@router.message(lambda message: message.text == '/father')
async def father_handler (message: types.Message):
    await message.answer(
        text = 'Меня создал великолепниший человек, человек с большой буквы, лучший из своего вида @Dan4oke'
    )

@router.message(Command("feedback"))
async def h_feedback(message: types.Message):    
    await message.answer(
        text=fedback_message
    )

@router.message(Command("ch__update_table__ch"))
async def updating_db_handl(message: types.Message):
    if str(message.from_user.id) == user_id_adm:
        await reader_gs()        
        await message.answer(
            text="обновление базы данных завршено"
        )

@router.message(Command("probability"))
async def probable(message: types.Message):
    await message.answer(
        "Выберите игру",
        reply_markup=mini_games
    )