from aiogram import types, Router
from config import username_bota
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext
from db import (
    Starosta
)
from keyboards import edit_strst, home_admin, kb_srsts
from FSMs import ForEditStName, ForDelStName

router= Router()

@router.callback_query(lambda c: c.data =='edit_starst')
async def edit_starst (callback: types.CallbackQuery):
    await callback.message.edit_text(
        text = "Смена старосты подразумевает очистку ячейки от id прежнего старосты, этого старосты\
        \nУдаление же повлечет за собой полное удаление и старосты и его подопечных, однако это\
        удаление не повлечет за собой тяжких последствий т.к. бот не может изменять главную таблицу",
        reply_markup= edit_strst
    )

@router.callback_query(lambda c: c.data == 'del_strst')
async def del_strst_handl (callback: types.CallbackQuery, state: FSMContext):
    markup = await kb_srsts()    
    await state.set_state(ForDelStName.for_del_name)
    await callback.message.edit_text(
        text= "Выберите старосту",
        reply_markup= markup
    )

@router.message(ForDelStName.for_del_name)
async def del_strst_handl1(message: types.Message, state:FSMContext):
    text = message.text
    await state.update_data(name = text)
    strst= Starosta()
    strst.set_other_atributs(name=text)
    strst.fool_del()
    await message.answer("Староста и его подопечные удалены", reply_markup=home_admin)

@router.callback_query(lambda c: c.data == "replace_strst")
async def replace_id0 (callback: types.CallbackQuery, state: FSMContext):
    markup = await kb_srsts()    
    await state.set_state(ForEditStName.for_edit_name)
    await callback.message.edit_text(
        text= "Выберите старосту",
        reply_markup= markup
    )
    await callback.message.answer(
            text= "Если вы передумали нажмите на кнопку ниже",
            reply_markup=home_admin
        )

@router.message(ForEditStName.for_edit_name)
async def replace_id(callback: types.CallbackQuery):    
    
    await callback.message.edit_text(
        text= "Теперь прежний староста не будет иметь доступ к данным",
        reply_markup= home_admin
    )