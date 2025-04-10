from datetime import datetime, timedelta

async def actualitic_date(date1):
    cur_date = datetime.now()
    #formated_datetime = cur_date.strftime("%Y-%m-%d %H:%M")

    if isinstance(date1, str):
        date1 = datetime.strptime(date1, "%Y-%m-%d %H:%M")
    
    if date1 > cur_date:
        return 'active'
    return 'NonActive'

async def raznica_time (date1) -> timedelta:
    cur_date = datetime.now()    

    if isinstance(date1, str):
        date1 = datetime.strptime(date1, "%Y-%m-%d %H:%M")
    
    razn = cur_date-date1
    return razn