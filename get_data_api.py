from typing import Tuple, Any, List, Dict

import requests
import json

from loger_util import logger


def get_catalog_code_car(vin_car) -> tuple[int, str, str]:
    """
    Функция для получения кода машины в каталоге сайта
    :param vin_car: vin номер полученный от пользователя.
    :return:    Status_code: Номер ошибки или ответа от сервера.
                Catalog_number_car: Номер машины в каталоге.
                Ssd_car: Токен передающийся с запросом.
    """

    url_search_catalog_number_car = (f'https://catalogoriginal.autodoc.ru/api/catalogs/original/cars/{vin_car}'
                                     f'/modifications?clientId=375')
    catalog_number_car = ''
    ssd_car = ''
    status_code = 0
    logger.info('Запрос кода машины')

    try:
        response = requests.get(url_search_catalog_number_car)
        status_code = response.status_code
    except ValueError as e:
        # не получается сделать запрос на сайт.
        status_code = 0
        return status_code, catalog_number_car, ssd_car
    else:
        if status_code == 200:
            try:
                data_catalog_number_car = json.loads(response.text)

                for attr in data_catalog_number_car["commonAttributes"]:
                    if attr['key'] == "Catalog":
                        catalog_number_car = attr['value']
                    if attr['key'] == "Ssd":
                        ssd_car = attr['value']

                return status_code, catalog_number_car, ssd_car

            except ValueError as e:
                # "Ошибка при декодировании JSON
                status_code = 1
                return status_code, catalog_number_car, ssd_car
        else:
            # Могут быть разные ошибки
            if response.status_code == 400:
                status_code = 400
                return status_code, catalog_number_car, ssd_car
                # "Ошибка 400: Неверный запрос. Проверьте параметры и данные запроса."
            elif response.status_code == 404:
                status_code = 404
                return status_code, catalog_number_car, ssd_car
            elif response.status_code == 503:
                status_code = 503
                return status_code, catalog_number_car, ssd_car
        return status_code, catalog_number_car, ssd_car


def get_car_info(catalog_number_car, ssd_car) -> tuple[int, dict]:
    """
    Функция для получения информации о машине
    :param catalog_number_car: Номер машины в каталоге.
    :param ssd_car: Токен передающийся с запросом.
    :return:    Status_code: Номер ошибки или ответа от сервера
                car_info: Информация о машине
    """

    car_info = {}
    url_search_car_info = (f"https://catalogoriginal.autodoc.ru/api/catalogs/original/catalogCodes/{catalog_number_car}"
                           f"?ssd={ssd_car}")

    try:
        response = requests.get(url_search_car_info)
        data_car_info = json.loads(response.text)
        status_code = response.status_code
    except ValueError as e:
        # Не получается получить данные о машине
        status_code = 1
        return status_code, car_info
    else:
        car_info = {
            'brand': data_car_info["items"][0]['brand'],
            'model': data_car_info["items"][0]['name'],
            'release_date': data_car_info["items"][0]['date'][0:4]
        }
        return status_code, car_info


def get_car_details(catalog_number_car, ssd_car) -> tuple[int, list[dict[str, Any]]]:
    """Функция для получения списка деталей
    :param catalog_number_car: номер машины в каталоге
    :return: car_info: информация о машине
    """
    url_search_car_details = (f'https://catalogoriginal.autodoc.ru/api/catalogs/original/brands/{catalog_number_car}'
                              f'/cars/0/quickgroups?ssd={ssd_car}')
    car_details = []

    try:
        response = requests.get(url_search_car_details)
        data_car_details = json.loads(response.text)
    except ValueError as e:
        # Не получается получить данные о деталях
        status_code = 1
        return status_code, car_details
    else:
        status_code = 0
        for item in data_car_details["data"][0]['children']:
            car_details.append({
                'name': item['name'],
                "quick_group_id": item['quickGroupId']
            })
        return status_code, car_details


def get_article_details(catalog_number_car, quick_group_id, ssd_car) -> tuple[int, list]:
    """Функция для получения артикулов деталей
        :param ssd_car:
        :param catalog_number_car: номер машины в каталоге
        :param quick_group_id: номер группы с типом детали(масляный фильтр, свечи зажигания...)
        :return: car_article: названия деталей и артикулы
    """
    url_search_car_article = (f'https://catalogoriginal.autodoc.ru/api/catalogs/original/brands/{catalog_number_car}'
                              f'/cars/0/quickgroups/{quick_group_id}/units')
    car_article = []

    try:
        # Данные для отправки в запросе POST
        payload = {
            'ssd': ssd_car,
        }
        # Выполнение POST-запроса
        response = requests.post(url_search_car_article, json=payload)
        status_code = response.status_code

    except ValueError as e:
        # Не получается получить данные об артикулах
        status_code = 1
        return status_code, car_article
    else:
        # Проверка статуса ответа
        if response.status_code == 200:
            try:
                data_car_article = response.json()
                # Массив для хранения нужных данных
                car_article = []

                # Обработка данных
                i = 0
                for item in data_car_article["items"]:
                    car_article.append({'code': item['code'], 'name': item['name'], 'details_info': []})
                    for details_info in item["spareParts"]:
                        if 'match' in details_info:
                            car_article[i]['details_info'].append(
                                {'name': details_info['name'], 'partNumber': details_info['partNumber']})
                    i = i + 1

                return status_code, car_article
            except ValueError as e:
                # "Ошибка при декодировании JSON
                status_code = 1
                return status_code, car_article
        else:
            # Могут быть разные ошибки
            if response.status_code == 400:
                status_code = 400
                return status_code, car_article
                # "Ошибка 400: Неверный запрос. Проверьте параметры и данные запроса."
            elif response.status_code == 404:
                status_code = 404
                return status_code, car_article
            elif response.status_code == 503:
                status_code = 503
                return status_code, car_article
            else:
                status_code = 1
                return status_code, car_article


# Дальше идет код только для тестирования
# @LOGER_UTILS.catch()
# def test_function(vin_car, quick_group_id):
#     status_code, catalog_number_car, ssd_car = get_catalog_code_car(vin_car)
#     LOGER_UTILS.debug("catalog_number_car: {}", catalog_number_car, "\nssd: {}", ssd_car)
#
#     status_code, car_info = get_car_info(catalog_number_car, ssd_car)
#     status_code, car_details = get_car_details(catalog_number_car, ssd_car)
#     LOGER_UTILS.debug("car_info: {}", car_info)
#     LOGER_UTILS.debug("car_details: {}", car_details)
#
#     status_code, article_details = get_article_details(catalog_number_car, quick_group_id, ssd_car)
#     LOGER_UTILS.debug("article_details: {}", article_details)


#
# quick_group_id = 2
# vin_car = 'Z8NAJL00050366148'
#
# test_function(vin_car, quick_group_id)
