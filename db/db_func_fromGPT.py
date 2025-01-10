import aiosqlite
from random import randint
import traceback
from config import get_db_connection


# Универсальная функция выполнения SELECT-запросов
async def execute_select_query(query: str, params: tuple = ()):
    async with aiosqlite.connect(get_db_connection()) as db:
        async with db.execute(query, params) as cursor:
            return await cursor.fetchall()

# Универсальная функция выполнения изменений в БД
async def execute_write_query(query: str, params: tuple = ()):
    try:
        async with aiosqlite.connect(get_db_connection()) as db:
            async with db.cursor() as cursor:
                await cursor.execute(query, params)
                await db.commit()
    except Exception as e:
        print("Произошла ошибка:", traceback.format_exc())

# Получение всех строк с определенными колонками, которые удовлетворяют какому-то условию
async def get_rows_by_condition(table: str, condition_column: str, condition_value: str):
    # Формируем SQL-запрос, выбирая только нужные колонки
    query = f"SELECT name, count_b FROM {table} WHERE {condition_column} = ?"
    params = (condition_value,)
    
    # Выполняем запрос с помощью существующей функции
    rows = await execute_select_query(query, params)
    
    # Возвращаем результат в виде списка списков
    return [list(row) for row in rows]  # Преобразуем кортежи в списки

# Получение всех строк колонки, которых удовлетворяют какому то условию
async def get_rows_for_statik():
    # Формируем SQL-запрос
    query = f"SELECT name, count_b FROM Just_users"    
    
    # Выполняем запрос с помощью существующей функции
    rows = await execute_select_query(query)
    
    # Возвращаем результат в виде списка списков
    return [list(row) for row in rows]  # Преобразуем кортежи в списки

# Получение всех значений колонки
async def get_all(table: str, column: str):
    query = f"SELECT {column} FROM {table}"
    rows = await execute_select_query(query)
    return [row[0] for row in rows]

# Получение значений по условию
async def get_all_if(table: str, column: str, condition_column: str, condition_value: str) ->list:
    query = f"SELECT {column} FROM {table} WHERE {condition_column} = ?"
    rows = await execute_select_query(query, (condition_value,))
    return [row[0] for row in rows]

# Обновление значения в таблице
async def update_value(table: str, column: str, value: str, condition_column: str, condition_value: str):
    query = f"UPDATE {table} SET {column} = ? WHERE {condition_column} = ?"
    await execute_write_query(query, (value, condition_value))

# Добавление нового пользователя
async def create_new_user(table: str, code: int, name: str, place: str):
    query = f"INSERT INTO {table} (unic_kod, name, place) VALUES (?, ?, ?)"
    await execute_write_query(query, (code, name, place))

# Добавление нового пользователя
async def create_new_user2(
        code: int, name: str, count_b:int,
        comment: str, unic_kod_strtsi: int
):
    query = f"INSERT INTO Just_users (unic_kod, name, count_b, comment, unic_kod_strtsi) VALUES (?, ?, ?, ?, ?)"
    await execute_write_query(query, (code, name, count_b, comment, unic_kod_strtsi))

# Проверка наличия значения в БД
async def exists_in_db(table: str, column: str, value: str):
    query = f"SELECT {column} FROM {table}"
    rows = await execute_select_query(query)
    return value in [row[0] for row in rows]

# Получение списка уникальных кодов
async def get_codes(table: str):
    return await get_all(table, "unic_kod")

# Создание уникального кода
async def create_code(table: str, start: int, end: int):
    while True:
        code = randint(start, end)
        codes = await get_codes(table)
        if code not in codes:
            return code

# Запись user_id
async def update_user_id(table: str, user_id: int, unic_kod: int):
    await update_value(table, "tg_user_id", user_id, "unic_kod", unic_kod)

# Получение значения по условиям
async def get_value_by_condition(table: str, column: str, condition_column: str, condition_value: str):
    query = f"SELECT {column} FROM {table} WHERE {condition_column} = ?"
    result = await execute_select_query(query, (condition_value,))
    return result[0][0] if result else None

# Получение всей строки по условиям
async def get_row_by_condition(table: str, condition_column: str, condition_value: str):
    query = f"SELECT * FROM {table} WHERE {condition_column} = ?"
    result = await execute_select_query(query, (condition_value,))
    return result[0] if result else None


# Удаление строки из БД
async def delete_from_db(table: str, condition_column: str, condition_value: str):
    query = f"DELETE FROM {table} WHERE {condition_column} = ?"
    await execute_write_query(query, (condition_value,))
