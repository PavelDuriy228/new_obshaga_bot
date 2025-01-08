import re
from db import (
    get_all
)

# Проверка нового старосты по маске
async def checking_starst (text:str) -> bool:
    pattern  = r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+:\s[0-9]+этаж\(\w+(\s*\/\s*\w+)?\)$'
    return bool(re.match(pattern, text))


