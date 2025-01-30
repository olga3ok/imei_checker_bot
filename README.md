# IMEI Checker Bot

## Описание

IMEI Checker Bot — это проект, который включает в себя Telegram-бота (aiogram) и бэкенд (FastAPI) для проверки IMEI. Бот позволяет пользователям отправлять IMEI и получать информацию о них, используя внешний API (https://imeicheck.net/) для проверки IMEI. Бот настроен для работы в Sandbox API Environment.

## Функциональность

- Проверка IMEI через Telegram-бота
- Проверка корректности IMEI
- Кэширование результатов запросов с использованием Redis
- Получение списка доступных сервисов

## Запуск

1. Клонируйте репозиторий:

    ```
    git clone https://github.com/olga3ok/imei_checker_bot.git
    cd imei_checker_bot
    ```

2. Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта и добавьте следующие переменные:

```env
TELEGRAM_BOT_TOKEN = ""
IMEI_CHECK_API_TOKEN = ""
IMEI_CHECK_API_URL = "https://api.imeicheck.net/v1/"
REDIS_URL = "redis://redis:6379"
BACKEND_URL = "backend"
```
В bot/whitelist.py добавьте нужные telegram ID для доступа к боту

3. Запуск docker-compose:
   ```
   docker-compose up --build
   ```
## Примеры запросов к API
### Проверка IMEI
- URL: /api/check-imei
- Метод: POST
- Пример:
```
curl -X POST http://localhost:8000/api/check-imei \
     -H "Content-Type: application/json" \
     -d '{"imei": "356735111052198"}'
```
### Получение списка доступных сервисов
- URL: /api/get-services
- Метод: GET
- Пример:
  ```
  curl -X GET http://localhost:8000/api/get-services
```


