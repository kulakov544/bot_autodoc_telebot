import requests
import json
from loguru import logger


logger.add("debag.log", format="{time} {level} {message}")


def get_catalog_code_car(vin_car):
    '''Функция
    :param vin_car: vin омер полученный от пользователя
    :return catalog_namber_car, ssd_car: номер машины в каталоге, токен передающийся с запросом
    '''

    url_search_catalog_namber_car = f'https://catalogoriginal.autodoc.ru/api/catalogs/original/cars/{vin_car}/modifications?clientId=375'
    response = requests.get(url_search_catalog_namber_car)


    if response.status_code == 200:
        try:
            data_catalog_namber_car = json.loads(response.text)

            for attr in data_catalog_namber_car["commonAttributes"]:
                if attr['key'] == "Catalog":
                    catalog_namber_car = attr['value']
                if attr['key'] == "Ssd":
                    ssd_car = attr['value']

            return catalog_namber_car, ssd_car

        except ValueError as e:
            #"Ошибка при декодировании JSON
            return 0, 0
    else:
        #Могут быть разные ошибки
        if response.status_code == 400:
            return 0, 400
            #"Ошибка 400: Неверный запрос. Проверьте параметры и данные запроса."
        elif response.status_code == 404:
            return 0, 404
        elif response.status_code == 503:
            return 0, 503
    return 0, 0


def get_car_info(catalog_namber_car, ssd_car):
    '''Функция
    :param catalog_namber_car, ssd_car: номер машины в каталоге
    :return car_info: информация о машине
    '''
    url_search_car_info = f'https://catalogoriginal.autodoc.ru/api/catalogs/original/catalogCodes/{catalog_namber_car}?ssd={ssd_car}'
    response = requests.get(url_search_car_info)

    data_car_info = json.loads(response.text)

    for item in data_car_info["items"]:
        car_info = {
            'brand': item['brand'],
            'model': item['name'],
            'release_date': item['date'][0:4]
        }

    return car_info


def get_car_details(catalog_namber_car, ssd_car):
    '''Функция
    :param catalog_namber_car: номер машины в каталоге
    :return car_info: информация о машине
    '''
    url_search_car_details = f'https://catalogoriginal.autodoc.ru/api/catalogs/original/brands/{catalog_namber_car}/cars/0/quickgroups?ssd={ssd_car}'
    response = requests.get(url_search_car_details)
    data_car_details = json.loads(response.text)
    car_details = []

    for item in data_car_details["data"][0]['children']:
        car_details.append({
            'name': item['name'],
            "quickGroupId": item['quickGroupId']
        })

    return car_details


def get_articl_details(catalog_namber_car, quickGroupId, ssd_car):
    '''Функция
        :param catalog_namber_car, quickGroupId: номер машины в каталоге, номер группы с типом детали(маслянный фильтр, свечи зажигания...)
        :return car_articl: названия деталей и артикулы
    '''
    url_search_car_articl = f'https://catalogoriginal.autodoc.ru/api/catalogs/original/brands/{catalog_namber_car}/cars/0/quickgroups/{quickGroupId}/units'
    # Данные для отправки в запросе POST
    payload = {
        'ssd': ssd_car,
    }
    # Выполнение POST-запроса
    response = requests.post(url_search_car_articl, json=payload)

    # Проверка статуса ответа
    if response.status_code == 200:
        try:
            data_car_articl = response.json()
            # Массив для хранения нужных данных
            car_articl = []

            # Обработка данных
            i = 0
            for item in data_car_articl["items"]:
                car_articl.append({'code': item['code'], 'name': item['name'], 'details_info': []})
                for details_info in item["spareParts"]:
                    if 'match' in details_info:
                        car_articl[i]['details_info'].append({'name': details_info['name'], 'partNumber': details_info['partNumber']})
                i = i+1

            return car_articl
        except ValueError as e:
            # "Ошибка при декодировании JSON
            return 0


#Дальше идет код только для тестирования
@logger.catch()
def test_function(vin_car, quickGroupId):
    catalog_namber_car, ssd_car = get_catalog_code_car(vin_car)
    logger.debug("catalog_namber_car: ", catalog_namber_car, "\nssd: ", ssd_car)
    print("catalog_namber_car: ", catalog_namber_car, "\nssd: ", ssd_car)

    car_info = get_car_info(catalog_namber_car, ssd_car)
    car_details = get_car_details(catalog_namber_car, ssd_car)
    logger.debug("car_info: ", car_info)
    print("car_info: ", car_info)
    print("car_details: ", car_details)

    articl_details = get_articl_details(catalog_namber_car, quickGroupId, ssd_car)
    logger.debug("articl_details: ", articl_details)
    print("articl_details: ", articl_details)


# quickGroupId = 2
# vin_car = 'VF1LA0H5324321010'
#
# test_function(vin_car, quickGroupId)