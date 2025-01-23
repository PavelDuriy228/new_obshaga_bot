from other_func import get_active_events, actualitic_date,raznica_time
from db import update_value, Event

async def actualitic_status ():
    active_events = await get_active_events()
    for event in active_events:
        status = await actualitic_date(date1=f"{event[3]} {event[4]}")
        if status != event[-1]:
            await update_value(
                table="Events",
                column='status', value=status,
                condition_column='unic_kod', condition_value=event[0]
            )
        razn = await raznica_time(date1=f'{event[3]} {event[4]}')
        if razn.days == 0:
            cls_event = await Event.set_by_id(id=event[0])
            if razn.total_seconds/3600 < 18_000:
                await cls_event.send_to_followers(text=f"До мероприятия {event[1]} осталос менее 5 часов")
            elif razn.total_seconds/3600 < 43_200:
                await cls_event.send_to_followers(text=f"До мероприятия {event[1]} осталос менее 12 часов")
            elif razn.total_seconds/3600 < 4000:
                await cls_event.send_to_followers(text=f"До мероприятия {event[1]} осталос менее часа")
            