
## О проекте
Телеграмм бот получает VIN номер автомобиля от пользователя. Ищет по нему информацию об автомобиле на сайте AutoDoc.ru. 
Выдает пользователю информацию об автомобиле и спрашивает какие детали для ТО требуются. 
Находит артикулы этих деталей и выдает пользователю.

Если вы хотите протестировать работу бота вы можете использовать следующие VIN номера:

-WAUBH54B11N111054  
-VF1LA0H5324321010  
-Z8NAJL00050366148  

### Техническое задание
Написать телеграмм-бота который будет принимать vin номер автомобиля и выдавать 
артикулы деталей для ТО взятые с сайта autodoc.ru.

### Решение
1. Бот запрашивает у пользователя VIN номер автомобиля(vin_car). 
2. Делает запрос на сайт и получает по нему данные для поиска машины в каталоге сайта.
   (catalog_number_car и ssd_car)
3. Делает запросы с этими данными и получает данные о машине(car_info) и 
данные по деталям которые необходимы для ТО этой машины(car_details).
4. Выводит в чат информацию о машине и кнопки с названиями деталей.
5. Пользователь выбирает какая деталь ему понадобится и нажимает кнопку.
6. Бот делает новый запрос к сайту в котором передает порядковый номер детали(quick_group_id),
и данные для поиска машины(catalog_number_car и ssd_car)
7. В ответ на запрос получает данные по выбранной детали(article_details)
8. Выводит в чат названия деталей и артикулы. Если для ТО выбранного узла нужно несколько деталей 
выведет их все в разных строчках.
9. После чего предложит выбрать другую деталь для этой машины.
10. В меню бота можно отправить команду старт, чтобы вернуться к началу работы с ботом.

![shema_autodoc_bot.png](images/shema_autodoc_bot.png)

## Используемые технологии

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![Telebot](https://img.shields.io/badge/Telebot-0.0.5+-yellow?logo=telegram)
![Requests](https://img.shields.io/badge/Requests-2.32.3+-orange?logo=python)

## Установка
Бот уже запущен на VPS сервере и работает постоянно. Его нужно просто найти: https://t.me/autodoc_articles_bot

Если вы хотите запустить его у себя следуйте инструкции:

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/kulakov544/bot_autodoc_telebot.git
   ```
2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
   ```
3. Установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Создайте файл .env в котором будет храниться токен телеграмм-бота
   ```
   BOT_TOKEN = "TOKEN"
   ```
5. Запустите программу.
   ```bash
   python main.py
   ```