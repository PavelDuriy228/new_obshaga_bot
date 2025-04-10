from other_func import get_active_events, actualitic_date,raznica_time
from db import update_value, Event

async def actualitic_status3 ():
    active_events = await get_active_events()
    for event in active_events:
        status = await actualitic_date(date1=f"{event[2]} {event[3]}")
        print(f'status: {status}')
        if status != event[-1]:
            await update_value(
                table="Events",
                column='status', value=status,
                condition_column='unic_kod', condition_value=event[0]
            )
        razn = await raznica_time(date1=f'{event[2]} {event[3]}')
        print(f"razn: {razn}")
        if razn.days == -1:
            cls_event = await Event.set_by_id(id=event[0])
            total_hours = int(razn.total_seconds())/ 3600 * (-1)
            # print(f'tot: hours: {total_hours}')
            
            if total_hours < 1:
                await cls_event.send_to_followers(
                    text=f'До мероприятия <b>{event[1]}</b>'\
' <span class="tg-spoiler">осталось менее часа</span>'                    
                )            
                
            
            elif 4 < total_hours < 5:
                await cls_event.send_to_followers(
                    text=f'До мероприятия <b>{event[1]}</b>'\
' <span class="tg-spoiler">осталось менее 5 часов</span>'
                    )                    
            
            elif 11 < total_hours < 12:
                await cls_event.send_to_followers(
                    text=f'До мероприятия <b>{event[1]}</b>'\
' <span class="tg-spoiler">осталось менее 12 часов</span>'
                )                   
    