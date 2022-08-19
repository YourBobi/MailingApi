# Сервис уведомлений

Приложение разработано на фреймворке django rest_framework

## Инструкция по настройке проекта:

1. Клонировать проект
```bash
git clone https://github.com/YourBobi/MailingApi.git
```

2. Открыть проект в PyCharm с наcтройками по умолчанию
3. Создать виртуальное окружение (через settings -> project "B1" -> project interpreter)
4. Открыть терминал в PyCharm, проверить, что виртуальное окружение активировано.
5. Обновить pip:
   ```bash
   pip install --upgrade pip
   ```
6. Установить в виртуальное окружение необходимые пакеты: 
   ```bash
   pip install -r requirements.txt
   ```

7. Синхронизировать структуру базы данных с моделями: 
   ```bash
   python manage.py migrate
   ```

8. Создать суперпользователя
   ```bash
   python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('kolya', 'abc@123.net', '123')"
   ```

9. Создать конфигурацию запуска в PyCharm (файл `manage.py`, опция `runserver`)

## Список api:
1. http://127.0.0.1:8000/api/v1/ -
2. http://127.0.0.1:8000/api/v1/clients/  - добавление клиентов
3. http://127.0.0.1:8000/api/v1/clients/detail/<int:pk>/ - удаление и изменение клиента
4. http://127.0.0.1:8000/api/v1/mailings - добавление рассылки
5. http://127.0.0.1:8000/api/v1/mailings/fullinfo/ - общая статистика
6. http://127.0.0.1:8000/api/v1/mailings/<pk>/info/ - детальная статистика
7. http://127.0.0.1:8000/api/v1/mailing/detail/<int:pk>/ - удаление и изменение рассылки
8. http://127.0.0.1:8000/api/v1/messages/ - добавление сообщения

