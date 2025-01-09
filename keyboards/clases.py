from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

class start_inl_kbs():    
    def __init__(self, unic_code:int):
        self.unic_code = unic_code
        pass

    # Стартовые кнопки для юзера
    async def user_buttons(self):
        button =InlineKeyboardButton("📈Статистка", callback_data=f"u_statistik:{self.unic_code}")
        return [
            [button]
        ]

    async def user_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("📈Статистка", callback_data=f"st_statistik:{self.unic_code}")]            
        ])                
        return keyboard
    
    async def star_buttons (self):
        button = InlineKeyboardButton("📈Статистка", callback_data=f"u_statistik:{self.unic_code}")        
        return [
            [button]            
        ]
    
    async def star_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📈Статистка", callback_data=f"st_statistik:{self.unic_code}")],
            [InlineKeyboardButton(text="Мои студенты", callback_data=f"my_students:{self.unic_code}:0:0")]
        ])        
        return keyboard
    
    async def home_star(self)-> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="В меню", callback_data=f"star_home_page:{self.unic_code}")]
        ])        
        return keyboard
    