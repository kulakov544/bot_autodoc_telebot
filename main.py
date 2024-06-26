import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import TOKEN
from get_data_api import get_data_car, get_articl_details, get_catalog_code_car


bot = telebot.TeleBot(TOKEN)
catalog_namber_car = ''
car_details = []
vin_car = ''

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Пожалуйста, отправьте VIN номер вашего автомобиля.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global car_info, car_details, catalog_namber_car
    vin_car = message.text.strip()
    if len(vin_car) == 17:  # Проверка корректности VIN номера
        catalog_namber_car = get_catalog_code_car(vin_car)
        if catalog_namber_car == 0:
            bot.reply_to(message, "Загрузка данных не получилась. Попробуйте ввести другой VIN.")
            send_welcome(message)

        else:
            car_info, car_details = get_data_car(vin_car)
            if car_info:
                reply_car_info = f'Марка: {car_info['brand']}\nМодель: {car_info['model']}\nГод выпуска: {car_info['release_date']}'
                bot.reply_to(message, reply_car_info)

                send_keyboard(message)
            else:
                bot.reply_to(message, f"Не удалось получить данные для VIN номера:{vin_car}")
    else:
        bot.reply_to(message, "Пожалуйста, введите корректный VIN номер (17 символов).")


@bot.message_handler(func=lambda message: True)
def send_keyboard(message):
    global car_details, keyboard
    keyboard = InlineKeyboardMarkup()

    # Создание кнопок на основе списка items
    for item in car_details:
        button = InlineKeyboardButton(text=item['name'], callback_data=item['quickGroupId'])
        keyboard.add(button)
    bot.send_message(message.chat.id, "Выберите тип деталей:", reply_markup=keyboard)


# Обработчик нажатий на кнопок
@bot.callback_query_handler(func=lambda callback: True)
def callback_query(callback):
    if callback.data == "back":
        bot.send_message(callback.message.chat.id, "Выберите тип деталей:", reply_markup=keyboard)
    else:
        quickGroupId = callback.data
        articl_details = get_articl_details(catalog_namber_car, quickGroupId)

        for articl in articl_details:
            message_articl_details = f'{articl['code']}: {articl['name']}\n'
            bot.send_message(callback.message.chat.id, message_articl_details)
            for details_info in articl['details_info']:
                message_articl_details = f'Название детали: {details_info['name']}\nАртикль детали: {details_info['partNumber']}'
                bot.send_message(callback.message.chat.id, message_articl_details)

        keyboard_back = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text='Выбрать другой тип детали', callback_data="back")
        keyboard_back.add(button)
        bot.send_message(callback.message.chat.id, "Хотите выбрать другие детали?", reply_markup=keyboard_back)

# vin_car = 'WAUBH54B11N111054'
#https://t.me/aaqwe_test_bot

if __name__ == '__main__':
    bot.polling(none_stop=True)