from aiogram import types, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from keyboards import create_shkatulki, mini_games
from FSMs import ForLaplas
from math import sqrt, e

router = Router()

@router.callback_query(lambda c: c.data == "shkatulka")
async def schkatulka_game(callback: types.CallbackQuery):
    markup = await create_shkatulki()
    await callback.message.edit_text(
        "Выберите шкатулку",
        reply_markup= markup
    )

@router.callback_query(lambda c: c.data.startswith("win_shk:"))
async def schakatulka_end (callback: types.CallbackQuery):
    res = callback.data.split(":")[1]
    if res == "1":    
        text="Вы выиграли!!!"        
    else:    
        text="Вам не повезло("                
    await callback.message.edit_text(
        text=text,
        reply_markup=mini_games
    )

@router.callback_query(lambda c: c.data=="laplas")
async def laplas_handle(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ForLaplas.values)
    await callback.message.edit_text(
        text= 'Введите значение переменных\
         \nР=...; \nn=...; \nk=...;\
         \n\nПример ввода: 0.003; 1000; 2'        
    )

@router.message(ForLaplas.values)
async def laplas_handle2(message: types.Message, state: FSMContext):
    await state.update_data(values=message.text)
    try:
        values = message.text.split(";")
        print(values)
        valuse2 = [ float(x.strip()) for x in values]
        print(valuse2)
        p = valuse2[0]
        n = valuse2[1]
        k= valuse2[2]
        q = 1- p
        x = (k - n * p)/ sqrt(n*p*q)
        print("x ", x)
        fi = 2.718281**(x*x/2*(-1))/ sqrt(2*3.14)
        print("fi ", fi)
        pr= fi / sqrt(n*p*q)
        print("pr ", pr)
        await message.answer(
            text=f"P= {pr}\nfi= {fi} \nx= {x}",
            reply_markup=mini_games
        )
    except Exception as e:
        print(e)
    await state.clear()
