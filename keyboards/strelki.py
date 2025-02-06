
async def create_strelki(len_list:int, callback_data:str, id, page):
    keyboard = []
    if page+1<len_list and page-1>-1:
            keyboard.append([
                InlineKeyboardButton(text="⬅️", callback_data=f"users_events:{id}:{page-1}"),
                InlineKeyboardButton(text="➡️", callback_data=f"users_events:{id}:{page+1}")       
            ])
        # ТОлько вперед
        if page +1 < len(list_id) and page-1 < 0:
            keyboard.append([
                InlineKeyboardButton(text="➡️", callback_data=f"users_events:{id}:{page+1}")        
            ])
        # ТОлько назад
        if page +1 >= len(list_id) and page-1 > -1:
            keyboard.append([
                InlineKeyboardButton(text="⬅️", callback_data=f"users_events:{id}:{page-1}")        
            ])   
    return keyboard         