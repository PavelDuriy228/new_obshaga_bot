from aiogram.types import InlineKeyboardButton

async def create_strelki(
    len_list:int, callback_dataU:str, page:int,
    range: int = 1
)-> list[InlineKeyboardButton] | None:   
    print(f"len_list: {len_list}") 
    print(f"callbacK: {callback_dataU}") 
    print(f"page: {page}")     
    if page+ range <len_list and page- range>-1:
        buttons = [
            InlineKeyboardButton(text="⬅️", callback_data=f"{callback_dataU}:{page-range}"),
            InlineKeyboardButton(text="➡️", callback_data=f"{callback_dataU}:{page+range}")       
        ]
    # ТОлько вперед
    elif page +range < len_list and page-range < 0:
        buttons = [
            InlineKeyboardButton(text="➡️", callback_data=f"{callback_dataU}:{page+range}")        
        ]
    # ТОлько назад
    elif page + range >= len_list and page- range > -1:
        buttons = [
            InlineKeyboardButton(text="⬅️", callback_data=f"{callback_dataU}:{page-range}")        
        ]
    else: return None
    return buttons