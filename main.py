import telebot
from config import TOKEN

from get_data_api import get_data_car


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Пожалуйста, отправьте VIN номер вашего автомобиля.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    vin_car = message.text.strip()
    if len(vin_car) == 17:  # Проверка корректности VIN номера
        car_info, car_details = get_data_car(vin_car)
        if car_info:
            reply = car_info
            bot.reply_to(message, car_info)
            bot.reply_to(message, car_details)
        else:
            bot.reply_to(message, f"Не удалось получить данные для VIN номера:{vin_car}")
    else:
        bot.reply_to(message, "Пожалуйста, введите корректный VIN номер (17 символов).")


# Запуск бота
bot.polling()
