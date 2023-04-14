# SomeStore

Проект SomeStore - интернет-магазин, позволяющий пользователям просматривать товары, добавлять их в корзину и оформлять заказы. Администраторы имеют возможность просматривать заказы, управлять товарами и пользователями. Проект разработан на Django и использует PostgreSQL в качестве базы данных. В проекте реализованы системы аутентификации и авторизации пользователей, а также возможность для администраторов модерировать заказы и товары.

## Структура проекта

Структура проекта выглядит следующим образом:

- `SomeStore/` - корневая директория проекта
    - `settings.py` - настройки проекта
    - `urls.py` - маршруты проекта
- `orders/` - приложение для заказов
    - `models.py` - модели для заказов и товаров
    - `serializers.py` - сериализаторы для моделей
    - `views.py` - контроллеры для заказов и товаров
    - `forms.py` - формы для создания и обновления заказов и товаров
    - `templates/` - шаблоны для представлений
    - `static/` - статические файлы приложения
- `users/` - приложение для пользователей
    - `models.py` - модели для пользователей
    - `views.py` - контроллеры для пользователей
    - `forms.py` - формы для создания и обновления пользователей

## Используемые технологии

- Python 3.8.0
- Django 4.1.7
- PostgreSQL 15.1
- Django REST Framework 3.14.0

## Установка и запуск проекта

1. Склонируйте репозиторий на свой компьютер:

```
git clone <https://github.com/Mikan-DS/SomeStore>

```

1. Перейдите в директорию проекта:

```
cd SomeStore

```

1. Создайте виртуальное окружение:

```
python -m venv venv

```

1. Активируйте виртуальное окружение:

Windows:

```
venv\\Scripts\\activate.bat

```

Linux / MacOS:

```
source venv/bin/activate

```

1. Установите зависимости:

```
pip install -r requirements.txt

```

1. Создайте базу данных:

```
python manage.py migrate

```

1. Создайте администратора:

```
python manage.py createsuperuser

```

1. Запустите сервер:

```
python manage.py runserver

```

1. Откройте браузер и перейдите по адресу `http://localhost:8000/`