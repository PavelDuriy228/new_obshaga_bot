from aiogram import  Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup,InlineKeyboardButton, Message
from aiogram.fsm.context import FSMContext
from FSMs import RepProblem
from other_func import send_to_adms
from db import User

router = Router()

@router.callback_query(lambda c: c.data.startswith("home_stud:"))
async def home_page_user (callback: CallbackQuery):
    cur_user_id = callback.from_user.id
    keyboard = InlineKeyboardMarkup(inline_keyboard=[            
            [InlineKeyboardButton(text="Мои мероприятия", callback_data=f"users_events:{cur_user_id}:0")]
        ])    
    await callback.message.edit_text(
        text= "Меню действий",
        reply_markup= keyboard
    )    

@router.callback_query(lambda c: c.data == "report_prob")
async def report_handler(callback: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=[        
        [InlineKeyboardButton(text="Назад", callback_data="user_menu")]
    ])
    await state.set_state(RepProblem.problem)

    await callback.message.edit_text(
        text="Напшите о проблеме которая у вас возникла",
        reply_markup=markup
    )    

@router.message(RepProblem.problem)
async def rep_problem2(message:Message, state: FSMContext):
    await state.clear()
    await send_to_adms(message=message)
    markup = InlineKeyboardMarkup(inline_keyboard=[        
        [InlineKeyboardButton(text="Назад", callback_data="user_menu")]
    ])
    await message.answer(
        text= "Ваше сообщение было отпарвлено администраторам",
        reply_markup=markup
    )


# @router.callback_query(lambda c: c.data.startswith("u_statistik:"))
# async def statistika_stud (callback: CallbackQuery):
#     unic_code =int(callback.data.split(":")[1])
#     user = await get_row_by_condition(
#         table="Just_users", condition_column='unic_kod',
#         condition_value=unic_code
#     )
#     text=f"{user[2]} \nБаллы:{user[3]}\n\nИстория:{user[4]}"
#     markup = start_inl_kbs(unic_code=unic_code)
#     n_markup = await markup.home_stud()
#     await callback.message.answer(
#         text="Посмотреть топ студентов по баллам", 
#         reply_markup= total_statistik
#     )
#     await callback.message.edit_text(
#         text = text,
#         reply_markup= n_markup
#     )    
