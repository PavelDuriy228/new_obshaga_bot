from db import update_value, get_value_by_condition, get_rows_by_condition_full

async def replacer(table:str, column:str, condition_column:str, condition_value, value_for_replace:str,value_to_replace:str):
    # Получаем ячейку
    getted_value = await get_value_by_condition(
        table=table, column=column, condition_column=condition_column,
        condition_value=condition_value
    )
    if value_for_replace !='_52nothing52_': new_value = str(getted_value).replace(value_for_replace, value_to_replace)
    else: new_value = f"{getted_value} {value_to_replace}"
    await update_value(
        table=table, 
        column=column, condition_column=condition_column,
        condition_value=condition_value, value=new_value
    )

async def get_active_events():
    rows = await get_rows_by_condition_full(
        table='Events',
        condition_column='status', condition_value='active', 
        columns='unic_kod, event_name, event_date, event_time, status'
    )
    return rows