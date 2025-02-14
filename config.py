import os
from dotenv import load_dotenv, find_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot
import sqlite3
from gspread import service_account 

load_dotenv(find_dotenv(), override=True)

Bot_token= os.getenv('token_test') # token_test token_master


# Получение ссылки на google таблицу
sheet_url = os.getenv('google_table')
print(sheet_url)
# API бота гугл таблиц
gc = service_account(filename="api_for_google_sheet.json")

# Пока нет новой ссылки
wks = gc.open("🔞Аттестация 2 2025/2025")


if Bot_token is None:
    raise ValueError("Токен бота не найден. Убедитесь, что переменная окружения 'token_test' установлена.")

bot = Bot(token = Bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

user_id_adm = os.getenv('user_id_adm') 
user_id_eventor = os.getenv('user_id_eventor')
username_bota = os.getenv('name_test')  #  name_master

current_dir= os.path.dirname(os.path.abspath(__file__))
def get_db_connection():
    db_path = os.path.join(current_dir, 'bali.db')
    return db_path

conn = sqlite3.connect(get_db_connection())
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Starst (
    unic_kod INT,
    tg_user_id INT,
    name TEXT,
    place TEXT, 
    created_works MEDIUMTEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Just_users (
    unic_kod INT,
    tg_user_id INT,
    name TEXT,
    count_b INT,
    comment MEDIUMTEXT,
    unic_kod_strtsi INT,
    code_events MEDIUMTEXT,
    code_of_works MEDIUMTEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Events (
    unic_kod INT,
    event_name TEXT,
    even_desription MEDIUMTEXT,               
    event_date DATE,
    event_time TIME,
    joined_users_id MEDIUMTEXT,
    joined_users_username MEDIUMTEXT,
    status TEXT      
)
''')