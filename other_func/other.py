from other_func import checking_time
from rapidfuzz import  process
from db import get_all, get_row_by_condition

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