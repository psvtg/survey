# Тестовое задание для компании Фабрика Решний

REST API приложения «Система опроса пользователей»

Использованный стек:
* Python 3.8.5
* Django 2.2.10
* django-rest-framework 3.12.4
* sqlite3

#### Files structure

- **api** - Django приложение с самим api
  - **admin.py** - Настройки админки Django
  - **models.py** - Модели приложения
  - **serializers.py** - Сериализаторы
  - **urls.py** - Описанием url'ов приложения
  - **views.py** - Файл с вью

#### API structure

Авторизация по логину и паролю в заголовке запроса.

`/api/surveys/` `[GET]` - Просмотр непройденных респондентом опросов


`/api/surveys/<int:id>/` `[GET]` - Просмотр опроса и его вопросов. id - id опроса


`/api/surveys/<int:id>/` `[POST]` - Прохождение опроса. Ответы на вопросы принимаются из request.data. Формат: {q1: 'мой ответ'}, где 1 - id вопроса. id - id опроса.
    
    Args: `q1`(str), `q4`(str) etc.


`/api/surveys/create/` `[POST]` - Создание опроса (необходима авторизация)

    Args: `name`(str), `description`(str), `date_start`(str: '2000-01-01'), `date_finish`(str: '2000-01-01')


`/api/surveys/<int:id>/update/` `[PUT]` - Изменение параметров опроса. Дата начала опроса не изменяема. id - id опроса. (необходима авторизация) 

    Args: `name`(str), `description`(str), `date_finish`(str: '2000-01-01')

`/api/surveys/<int:id>/update/` `[DELETE]` - Удаление опроса. id - id опроса. (необходима авторизация)


`/api/surveys/<int:id>/questions/` `[POST]` - Добавление вопроса в опрос. id - id опроса. (необходима авторизация)

    Args: `question_id`(int)

`/api/surveys/<int:id>/questions/` `[PUT]` - Замена вопроса в опросе. id - id опроса. (необходима авторизация)

    Args: `question_old_id`(int), Args: `question_new_id`(int)
    

`/api/surveys/<int:id>/questions/` `[DELETE]` - Удаление вопроса и опроса. id - id опроса. (необходима авторизация)

    Args: `question_id`(int)
    

`/api/surveys/done` `[GET]` - Просмотр пройденных респондентом опросов.


Развертка проекта:

Тип: локально

`git clone 'https://github.com/psvtg/survey.git'`

`pip install -r requirements.txt`

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py createsuperuser`

`python manage.py runserver`
