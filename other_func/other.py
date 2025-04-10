from other_func import checking_time
from rapidfuzz import  process
from random import choice
from db import get_all, get_row_by_condition
from texts import spam_messages
from .adm_sup import send_for_all_func

async def splitter_time(date):
    print(date)
    checked = await checking_time(str(date))
    if checked:
        n_date = str(date).split(" ")[0].strip()
        time = str(date).split(" ")[1].strip()
        return [n_date, time]
    else:
        return False
    
async def search(query:str):    
    names = await get_all(
        table="Events",
        column='event_name'
    )
    best_match = process.extractOne(query, names)
    id = await get_row_by_condition(
        table='Events', 
        condition_column='event_name',
        condition_value=best_match[0]
    )
    return id[0]

async def sending_spam():        
    mess = choice(spam_messages)
    await send_for_all_func(
        text=mess
    )