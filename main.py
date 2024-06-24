import telebot
from dotenv import load_dotenv
import os

from get_data import get_car_info


load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Пожалуйста, отправьте VIN номер вашего автомобиля.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    vin_car = message.text.strip()
    if len(vin_car) == 17:  # Проверка корректности VIN номера
        car_data_info = get_car_info(vin_car)
        if car_data_info:
            reply = car_data_info
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, f"Не удалось получить данные для VIN номера:{vin_car}")
    else:
        bot.reply_to(message, "Пожалуйста, введите корректный VIN номер (17 символов).")

# Запуск бота
bot.polling()
