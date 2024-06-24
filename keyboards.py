from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

start = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Ввести новый VIN", callback_data='start_script')]]
)

# start = ReplyKeyboardMarkup(
#     keyboard=[[KeyboardButton(text="Ввести новый VIN"), KeyboardButton(text="История VIN номеров")]],
#     resize_keyboard=True
# )
# cars =[1, 2, 3]
# async def inline_cars():
#     keyboard = InlineKeyboardBuilder()
#     for car in cars:
#         keyboard.add(InlineKeyboardButton(text=car, url='https://yandex.ru/'))
#     return keyboard.adjust(1).as_markup()