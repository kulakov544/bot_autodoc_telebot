import telebot
from config import TOKEN

from get_data_api import get_data_car, get_articl_details


bot = telebot.TeleBot(TOKEN)
catalog_namber_car = ''
car_details = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Пожалуйста, отправьте VIN номер вашего автомобиля.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    vin_car = message.text.strip()
    if len(vin_car) == 17:  # Проверка корректности VIN номера
        car_info, car_details, catalog_namber_car = get_data_car(vin_car)
        if car_info:
            reply_car_info = f'Марка: {car_info['brand']}\nМодель: {car_info['model']}\nГод выпуска: {car_info['release_date']}'
            bot.reply_to(message, reply_car_info)
        else:
            bot.reply_to(message, f"Не удалось получить данные для VIN номера:{vin_car}")

        #Генерируем клавиатуру



    else:
        bot.reply_to(message, "Пожалуйста, введите корректный VIN номер (17 символов).")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global catalog_namber_car, car_details
    #получаем артикли деталей
    quickGroupId = 2
    get_articl_details(catalog_namber_car, quickGroupId)


    reply_car_info = f'Марка'
    bot.reply_to(message, reply_car_info)


# Запуск бота
bot.polling()
