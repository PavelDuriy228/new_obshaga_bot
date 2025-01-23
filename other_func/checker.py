import re
from datetime import datetime

# Проверка нового старосты по маске
async def checking_starst (text:str) -> bool:
    pattern  = r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+:\s[0-9]+этаж\(\w+(\s*\/\s*\w+)?\)$'
    return bool(re.match(pattern, text))


async def checking_time (date_string):
    # Попробуем распарсить строку как дату и время
    try:
        # Попробуйте изменить формат в зависимости от ваших требований
        datetime.strptime(date_string, '%Y-%m-%d %H:%M')  # Формат: YYYY-MM-DD HH:MM
        return True
    except ValueError:
        return False