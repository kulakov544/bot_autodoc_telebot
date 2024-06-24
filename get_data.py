from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def get_car_data(vin):
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

        # Нахождение и нажатие кнопки для раскрытия дополнительной информации
        button_car_info = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.button-info')))
        button_car_info.click()

        # Парсинг данных
        car_info_all = [driver.find_element(By.CSS_SELECTOR, '.view-dialog').text]
        car_info_all = car_info_all[0].split('\n')
        car_info = car_info_all[0]+'\n'+car_info_all[1]+'\n'+car_info_all[3]

        #print(car_info)

        return car_info
    except Exception as e:
        print(f"Ошибка: {e}")
        return None
    finally:
        driver.quit()


# vin_car = 'WAUBH54B11N111054'
# get_car_data(vin_car)
