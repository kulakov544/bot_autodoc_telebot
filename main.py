import telebot

from config import TOKEN
from keyboard import bild_keyboard_details, bild_keyboard_back
from get_data_api import (get_articl_details,
                          get_catalog_code_car,
                          get_car_info,
                          get_car_details)


bot = telebot.TeleBot(TOKEN)
user_data = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Пожалуйста, отправьте VIN номер вашего автомобиля.")
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {
            'vin_car': '',
            'catalog_number_car': '',
            'ssd_car': '',
            'car_info': [],
            'car_details': [],
            'articl_details': [],
            'keyboard_details': ''
        }


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    '''Функция
    Запрашивает vin(vin_car). находит номер машины в каталоге(catalog_namber_car) и ssd(токен для запросов ssd_car).
    По номеру машины находит информацию о машине(car_info) и список деталей для ТО(car_details).
    Выводит информацию о машине(reply_car_info) и клавиатуру со списком деталей(keyboard_details)
    '''

    user_id = message.from_user.id
    user_info = user_data.get(user_id, {})

    vin_car = message.text.strip()

    if len(vin_car) == 17:  # Проверка корректности VIN номера
        catalog_namber_car, ssd_car = get_catalog_code_car(vin_car)

        if ssd_car == 404:
            bot.reply_to(message, "Не удалось найти VIN номер в базе сайта. Проверьте что он верно введен, если он верен проведите поиск через сайт.")
            send_welcome(message)
        elif ssd_car == 400 or ssd_car == 0:
            bot.reply_to(message, "Ошибка запроса. Сообщите нам с каким vin номеров возникла проблема.")
            send_welcome(message)
        elif ssd_car == 503:
            bot.reply_to(message, "Сайт недоступен. Попробуйте позже.")
            send_welcome(message)
        else:
            car_info = get_car_info(catalog_namber_car, ssd_car)
            car_details = get_car_details(catalog_namber_car, ssd_car)

            if car_info:
                reply_car_info = f'Марка: {car_info['brand']}\nМодель: {car_info['model']}\nГод выпуска: {car_info['release_date']}'
                bot.reply_to(message, reply_car_info)

                keyboard_details = bild_keyboard_details(car_details)
                user_data[user_id].update({
                    'vin_car': vin_car,
                    'catalog_number_car': catalog_namber_car,
                    'ssd_car': ssd_car,
                    'car_info': car_info,
                    'car_details': car_details,
                    'articl_details': [],
                    'keyboard_details': keyboard_details
                })


                bot.send_message(message.chat.id, "Выберите тип деталей:", reply_markup=keyboard_details)
            else:
                bot.reply_to(message, f"Не удалось получить данные для VIN номера:{vin_car}")
    else:
        bot.reply_to(message, "Пожалуйста, введите корректный VIN номер (17 символов).")


# Обработчик нажатий на кнопок
@bot.callback_query_handler(func=lambda callback: True)
def callback_query(callback):
    '''Функция
    Обрабатывает нажатия на кнопки. Если выбрана деталь из списка деталей получает номер группы этой детали(quickGroupId) и
    артикулы всех деталей этой группы(articl_details). Выводит их в сообщении пользователю и предлагает выбрать ещё раз.
    '''
    user_id = callback.from_user.id
    user_info = user_data.get(user_id, {})

    if callback.data == "back":
        keyboard_details = user_info.get('keyboard_details', '')
        bot.send_message(callback.message.chat.id, "Выберите тип деталей:", reply_markup=keyboard_details)
    else:
        catalog_namber_car = user_info.get('catalog_number_car', '')
        ssd_car = user_info.get('ssd_car', '')

        quickGroupId = callback.data

        articl_details = get_articl_details(catalog_namber_car, quickGroupId, ssd_car)

        for articl in articl_details:
            message_articl_details = f'{articl['code']}: {articl['name']}\n'
            bot.send_message(callback.message.chat.id, message_articl_details)
            for details_info in articl['details_info']:
                message_articl_details = f'Название детали: {details_info['name']}\nАртикль детали: {details_info['partNumber']}'
                bot.send_message(callback.message.chat.id, message_articl_details)

        keyboard_back = bild_keyboard_back()
        bot.send_message(callback.message.chat.id, "Хотите выбрать другие детали?", reply_markup=keyboard_back)

'''
vin_car = 'WAUBH54B11N111054' VF1LA0H5324321010   Z8NAJL00050366148
vin_car = 'Z8NAJL00050366148'

autodoc_articles_bot
7450111568:AAGe4YKGaphh31oEzGELQ9FIOd9DaGY7mcA
'''


if __name__ == '__main__':
    bot.polling(none_stop=True)