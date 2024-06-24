from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def get_data_site(VIN):
    # Устанавливаем драйвер и запускаем браузер
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Открываем начальную страницу
        driver.get('https://www.autodoc.ru/catalogs/original/list-nodes/nodes?vin=' + VIN)

        # Ожидаем, пока элемент с кнопкой станет видимым
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.ID, 'button-id')))

        # Кликаем по кнопке для перехода на новую страницу
        button.click()

        # Ожидаем, пока новая страница загрузится
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'data-class')))

        # Извлекаем данные
        elements = driver.find_elements(By.CLASS_NAME, 'data-class')
        data = []
        for element in elements:
            title = element.find_element(By.TAG_NAME, 'h3').text
            description = element.find_element(By.TAG_NAME, 'p').text
            data.append({
                'title': title,
                'description': description
            })

        # Выводим результаты
        for item in data:
            data = 1
            print(f"Title: {item['title']}")
            print(f"Description: {item['description']}")
            print()

    finally:
        # Закрываем браузер
        driver.quit()

    return data

