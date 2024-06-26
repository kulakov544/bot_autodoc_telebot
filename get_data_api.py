import requests
import json


# URL API
url = "https://catalogoriginal.autodoc.ru/api/catalogs/original/catalogCodes/AU1519"

ssd = '$*KwGyhpe9xO_Os-6y0NWL4-r-3tnHt7C2sKeIu_P1xtHJz_jbqaS9wNbH0sLJs7Cb5vrOsLe2sLSy-q-yo8D6pOWiu6TFjPXnovLrpbqj09eY9eei4qS9sre3qPu66bqjx7GiraT3uvXxorXEtbXXzab19a7jo7ylwdXXpvX1v-OjvKXF29ym9fW96e-kvaLWx9Gbn_60w7e2zrC3teni_6KtpPOiu6TSkJmU09XUzsPVpPkAAAAAXWSxRg==$'


def get_catalog_code_car(vin_car):
    global catalog_namber_car
    url_search_catalog_namber_car = f'https://catalogoriginal.autodoc.ru/api/catalogs/original/cars/{vin_car}/modifications'
    response = requests.get(url_search_catalog_namber_car)
    data_catalog_namber_car = json.loads(response.text)

    for attr in data_catalog_namber_car["commonAttributes"]:
        if attr['key'] == "Catalog":
            catalog_namber_car = attr['value']

    return catalog_namber_car


def get_car_info(catalog_namber_car):
    global car_info
    url_search_car_info = f'https://catalogoriginal.autodoc.ru/api/catalogs/original/catalogCodes/{catalog_namber_car}?ssd={ssd}'
    response = requests.get(url_search_car_info)
    data_car_info = json.loads(response.text)

    for item in data_car_info["items"]:
        car_info = {
            'brand': item['brand'],
            'model': item['name'],
            'release_date': item['date'][0:4]
        }

    return car_info


def get_car_details(catalog_namber_car):
    global car_details
    url_search_car_details = f'https://catalogoriginal.autodoc.ru/api/catalogs/original/brands/{catalog_namber_car}/cars/0/quickgroups?ssd={ssd}'
    response = requests.get(url_search_car_details)
    data_car_details = json.loads(response.text)
    car_details = []

    for item in data_car_details["data"][0]['children']:
        car_details.append({
            'name': item['name'],
            "quickGroupId": item['quickGroupId']
        })

    return car_details


def get_articl_details(catalog_namber_car, quickGroupId):
    url_search_car_articl = f'https://catalogoriginal.autodoc.ru/api/catalogs/original/brands/{catalog_namber_car}/cars/0/quickgroups/{quickGroupId}/units'
    # Данные для отправки в запросе POST
    payload = {
        'ssd': ssd,
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
            print(f"Ошибка при декодировании JSON: {e}")
    else:
        print(f"Ошибка: {response.status_code}")
        print("Текст ответа:", response.text)
        if response.status_code == 400:
            print("Ошибка 400: Неверный запрос. Проверьте параметры и данные запроса.")




def get_data_car(vin_car):
    catalog_namber_car = get_catalog_code_car(vin_car)

    car_infо = get_car_info(catalog_namber_car)

    car_details = get_car_details(catalog_namber_car)

    return car_infо, car_details, catalog_namber_car


# vin_car = 'WAUBH54B11N111054'
#
# get_data_car(vin_car)