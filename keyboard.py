from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def bild_keyboard_details(car_details):
    keyboard_details = InlineKeyboardMarkup()
    # Создание кнопок на основе списка car_details
    for item in car_details:
        button = InlineKeyboardButton(text=item['name'], callback_data=item['quickGroupId'])
        keyboard_details.add(button)
    return keyboard_details

def bild_keyboard_back():
    keyboard_back = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='Выбрать другой тип детали', callback_data="back")
    keyboard_back.add(button)
    return keyboard_back