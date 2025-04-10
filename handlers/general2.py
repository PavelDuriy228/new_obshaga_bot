from aiogram import Router
from keyboards import etagi_inl, studsovet_urls
from db import get_all
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from other_func.viewer_studs import viewer_studs
from texts import studsovet_message, my_events_message, studsovet_list, studsovet_urls, default_photo_url
from keyboards.strelki import create_strelki
from keyboards import studsovet_urls as inline_studsovet_urls
from .sup_func import menu_func
from config import bot

router = Router()

@router.callback_query(lambda c: c.data == "user_menu")
async def handle_menu (callback: CallbackQuery):
    await menu_func(
        mes=callback
    )

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


@router.callback_query(lambda c: c.data.startswith("start_event:"))
async def star_students (callback: CallbackQuery):    
    tg_id = callback.data.split(":")[1]
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Далее", callback_data=f"users_events:{tg_id}:0")],
        [InlineKeyboardButton(text="Назад", callback_data="user_menu")]
    ])

    await callback.message.edit_text(
        text = my_events_message,
        reply_markup= markup
    )    

@router.callback_query(lambda c: c.data.startswith("studsovet:"))
async def studsovet_handl (callback: CallbackQuery):    
    flag = callback.data.split(":")[1]
    indx = int(callback.data.split(":")[2])
    keyboard = [await create_strelki(
        len_list=len(studsovet_urls),
        callback_dataU="studsovet:1", page=indx                
    )]
    keyboard.append(    
        inline_studsovet_urls[indx]        
    )
    # keyboard.append(
    #     [InlineKeyboardButton(text="Назад", callback_data="user_menu")]
    # )
    
    markup = InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
    if flag == "0":            
        # await bot.send_photo(
        #     chat_id=callback.from_user.id,
        #     photo=studsovet_urls[0],
        #     caption=studsovet_list[0],
        #     reply_markup=markup,
        #     parse_mode="html"
        # )
        markup2 = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="user_menu")]
        ])

        await callback.message.answer(
            text= studsovet_message,
            reply_markup= markup2
        )
    
    if studsovet_urls[indx] != "":
        photo = InputMediaPhoto(
            media=studsovet_urls[indx], caption=studsovet_list[indx],
            parse_mode="html"
        )    
            
    else:
        photo = InputMediaPhoto(
            media=default_photo_url, caption=studsovet_list[indx],
            parse_mode="html"
        )                            
            
    await callback.message.edit_media(
            media = photo,
            reply_markup= markup                
        )
