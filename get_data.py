from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging


def get_car_info(vin):
    # Настройки для работы Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Инициализация драйвера
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # URL сайта, на который будем заходить
        url = f'https://www.autodoc.ru/catalogs/original/list-nodes/nodes?vin={vin}'
        driver.get(url)

        # Ожидание загрузки страницы
        wait = WebDriverWait(driver, 5)

        # Нахождение и нажатие кнопки для раскрытия информации о машине
        button_car_info = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.button-info')))
        button_car_info.click()

        # Парсинг данных авто
        car_info_all = driver.find_element(By.CSS_SELECTOR, '.view-dialog').text.split('\n')
        car_info = f"{car_info_all[0]}\n{car_info_all[1]}\n{car_info_all[3]}"
        #print(car_info)

        #Нахождение и нажатие кнопки для раскрытия списка деталей
        # button_car_details = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.p-treenode-content.p-treenode-selectable.p-highlight')))
        # button_car_details.click()

        # Парсинг списка деталей
        # car_details = driver.find_element(By.CSS_SELECTOR, '//li[@class="p-treenode ng-star-inserted"]').text.split('\n')

        # print(car_details)

        return car_info

    except Exception as e:
        print(f"Ошибка: {e}")
        return None
    finally:
        driver.quit()




# vin_car = 'WAUBH54B11N111054'
# get_car_info(vin_car)
