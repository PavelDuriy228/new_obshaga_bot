from aiogram import Router
from keyboards import etagi_inl
from db import get_all
from aiogram.types import CallbackQuery
from other_func.viewer_studs import viewer_studs

router = Router()

@router.callback_query(lambda c: c.data=="choise_etag")
async def handl_of_choice_etag(callback: CallbackQuery):
    list_etags = await get_all(
        table="Starst",
        column="place"# сосочки Булата  Пирамидки Ани
    )
    list_id_etags = await get_all(
        table="Starst",
        column="unic_kod"
    )
    markup =await etagi_inl(
        etagi=list_etags,
        id_etag=list_id_etags
    )
    await callback.message.edit_text(
        text="Выберите этаж",
        reply_markup=markup
    )

@router.callback_query(lambda c: c.data.startswith("view_studs:"))
async def star_students (callback: CallbackQuery):    
    await viewer_studs(
        callback=callback
    )