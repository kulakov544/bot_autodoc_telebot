import telebot

from config import TOKEN
from keyboard import bild_keyboard_details, bild_keyboard_back
from loger_util import logger
from get_data_api import (get_article_details,
                          get_catalog_code_car,
                          get_car_info,
                          get_car_details)


bot = telebot.TeleBot(TOKEN)
user_data = {}

@logger.catch()
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Отправьте VIN номер автомобиля.")
    user_id = message.from_user.id
    logger.info('Появился новый пользователь: {}', user_id)
    if user_id not in user_data:
        user_data[user_id] = {
            'vin_car': '',
            'catalog_number_car': '',
            'ssd_car': '',
            'car_info': [],
            'car_details': [],
            'article_details': [],
            'keyboard_details': ''
        }


@logger.catch()
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Функция
    Запрашивает vin(vin_car). находит номер машины в каталоге(catalog_number_car) и ssd(токен для запросов ssd_car).
    По номеру машины находит информацию о машине(car_info) и список деталей для ТО(car_details).
    Выводит информацию о машине(reply_car_info) и клавиатуру со списком деталей(keyboard_details)
    """

    user_id = message.from_user.id
    user_info = user_data.get(user_id, {})
    logger.info("Пользователь {} передал вин", user_id)

    vin_car = message.text.strip()
    vin_car = vin_car.upper()

    if len(vin_car) == 17:  # Проверка корректности VIN номера
        status_code, catalog_number_car, ssd_car = get_catalog_code_car(vin_car)

        if status_code == 404:
            logger.error("ошибка в поиске машины: {}, для вин номера: {}", status_code, vin_car)
            bot.send_message(message.chat.id,
                             f"Не удалось найти VIN номер в базе сайта. Проверьте что он верно введен, если он "
                             f"верен проведите поиск через сайт:\nhttps://www.autodoc.ru/catalogs/original?"
                             f"findVin={vin_car}")
            bot.send_message(message.chat.id, "Отправьте VIN номер автомобиля.")
        elif status_code == 400 or status_code == 0:
            logger.error("ошибка в поиске машины: {}, для вин номера: {}", status_code, vin_car)
            bot.send_message(message.chat.id, "Ошибка запроса. Сообщите нам с каким vin номером возникла проблема.")
            bot.send_message(message.chat.id, "Отправьте VIN номер автомобиля.")
        elif status_code == 503:
            logger.error("ошибка в поиске машины: {}, для вин номера: {}", status_code, vin_car)
            bot.send_message(message.chat.id, "Сайт недоступен. Попробуйте позже.")
            bot.send_message(message.chat.id, "Отправьте VIN номер автомобиля.")
        elif status_code == 1:
            logger.error("ошибка в поиске машины: {}, для вин номера: {}", status_code, vin_car)
            bot.send_message(message.chat.id, "Ошибка запроса. Сообщите нам с каким vin номером возникла проблема.")
            bot.send_message(message.chat.id, "Отправьте VIN номер автомобиля.")
        else:
            status_code, car_info = get_car_info(catalog_number_car, ssd_car)
            status_code, car_details = get_car_details(catalog_number_car, ssd_car)

            if car_info:
                logger.debug("car_info: {}", car_info)
                logger.debug("car_details: {}", car_details)
                reply_car_info = f"Марка: {car_info['brand']}\nМодель: {car_info['model']}\nГод выпуска: {car_info['release_date']}"
                bot.send_message(message.chat.id, reply_car_info)
                logger.info("Информация по машине для пользователя {} найдена.", user_id)

                keyboard_details = bild_keyboard_details(car_details)
                user_data[user_id].update({
                    'vin_car': vin_car,
                    'catalog_number_car': catalog_number_car,
                    'ssd_car': ssd_car,
                    'car_info': car_info,
                    'car_details': car_details,
                    'article_details': [],
                    'keyboard_details': keyboard_details
                })

                bot.send_message(message.chat.id, "Выберите тип деталей:", reply_markup=keyboard_details)
            else:
                logger.error("ошибка в поиске машины: {}", status_code)
                bot.send_message(message.chat.id, f"Не удалось получить данные для VIN номера:{vin_car}")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректный VIN номер (17 символов).")


# Обработчик нажатий на кнопок
@bot.callback_query_handler(func=lambda callback: True)
def callback_query(callback):
    """Функция
    Обрабатывает нажатия на кнопки. Если выбрана деталь из списка деталей получает номер группы этой детали(quick_group_id) и
    артикулы всех деталей этой группы(article_details). Выводит их в сообщении пользователю и предлагает выбрать ещё раз.
    """
    user_id = callback.from_user.id
    user_info = user_data.get(user_id, {})

    if callback.data == "back":
        keyboard_details = user_info.get('keyboard_details', '')
        bot.send_message(callback.message.chat.id, "Выберите тип деталей:", reply_markup = keyboard_details)
    else:
        catalog_number_car = user_info.get('catalog_number_car', '')
        ssd_car = user_info.get('ssd_car', '')

        quick_group_id = callback.data

        status_code, article_details = get_article_details(catalog_number_car, quick_group_id, ssd_car)
        if status_code == 200:
            for article in article_details:
                message_article_details = f"{article['code']}: {article['name']}\n"
                bot.send_message(callback.message.chat.id, message_article_details)
                for details_info in article['details_info']:
                    message_article_details = f"Название детали: {details_info['name']}\nАртикул детали: {details_info['partNumber']}"
                    bot.send_message(callback.message.chat.id, message_article_details)
            logger.info("Вывод артикулов деталей: {}", article_details)
            keyboard_back = bild_keyboard_back()
            bot.send_message(callback.message.chat.id, "Хотите выбрать другие детали?", reply_markup=keyboard_back)
        elif status_code == 1:
            logger.error("ошибка в поиске артикулов: {}, для вин номера: {}", status_code, user_info.get('vin_car', ''))
            bot.send_message(callback.chat.id, "Ошибка запроса. Сообщите нам с каким vin номером возникла проблема.")
            bot.send_message(callback.chat.id, "Отправьте VIN номер автомобиля.")


if __name__ == '__main__':
    logger.info('Старт бота.')
    bot.polling(none_stop=True)
