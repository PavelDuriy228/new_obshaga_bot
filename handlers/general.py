from aiogram import types, Router
from config import user_id_adm, user_id_eventor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from .sup_func import set_id_new_user, chosing_role
from keyboards import adm_menu_markup, eventor_markup, total_statistik, mini_games
from db import reader_gs, reader_old_table, get_all, create_new_user3

router = Router()

@router.message(CommandStart())
async def h_start (message:types.Message, state:FSMContext, command: CommandStart):
    # Получение кода при старте бота
    unic_code = command.args
    cur_user_id = message.from_user.id
    # Очистка всех Машин состояний
    await state.clear()
    await message.answer("Этот бот создан для учета баллов в общежитии", reply_markup= types.ReplyKeyboardRemove())
    await message.answer("Нажмите на эту кнопку, чтобы посмотреть полную статистике по общежитию", reply_markup=total_statistik)

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
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[            
        [InlineKeyboardButton(text="Мои мепрориятия", callback_data=f"users_events:{cur_user_id}:0")]
    ])
    await message.answer(
        'Здравствуйте, выберите вот ваше меню действий',
        reply_markup=keyboard
    )
    if cur_user is not None:
        # Приветственное сообщение с менюшкой
        await cur_user.say_my_name(message=message)
    if str(cur_user_id) == user_id_adm:
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
        text="Если возникли какие либо трудности или есть идеи,\
        пишите мне в лс @I_Pavel_Durov, я обязательно отвечу"
    )

@router.message(Command("ch__update_table__ch"))
async def updating_db_handl(message: types.Message):
    if str(message.from_user.id) == user_id_adm:
        await reader_gs()
        await reader_old_table()
        await message.answer(
            text="обновление базы данных завршено"
        )

@router.message(Command("probability"))
async def probable(message: types.Message):
    await message.answer(
        "Выберите игру",
        reply_markup=mini_games
    )