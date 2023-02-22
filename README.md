# Спринт 5 - Протестируйте проект Yatube
Покрытие тестами проекта Yatube из спринта 4

## Для запуска приложения в dev-режиме проделайте следующие шаги:
1) Склонируйте репозиторий.

2) Перейдите в папку с кодом и создайте виртуальное окружение:
~~~
python -m venv venv
~~~

3) Активируйте виртуальное окружение:
~~~
source venv/Scripts/activate
~~~

4) Установите зависимости:
~~~
python -m pip install -r requirements.txt
~~~

5) Выполните миграции:
~~~
python manage.py makemigrations

python manage.py migrate
~~~

6) Создайте суперпользователя:
~~~
python manage.py createsuperuser
~~~

7) Запустите сервер:
~~~
python manage.py runserver
~~~
