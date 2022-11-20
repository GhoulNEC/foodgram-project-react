![yamdb_workflow](https://github.com/GhoulNEC/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Foodgram-project

[Ссылка](http://recipes-book.serveblog.net/recipes) на проект.

***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Описание</summary>

Проект Foodgram позволяет публиковать рецепты блюд. Для удобства отслеживания 
рецептов реализованы системы подписки на авторов и добавления рецептов в избранное.
Так же у пользователя есть корзина, в которую он может добавить понравившиеся рецепты
и скачать список продуктов.
</details>

***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Технологии</summary>

* Python 3.8.9
* Django 2.2.16
* djangorestframework 3.12.4
* PostgreSQL
* nginx
* gunicorn
* Docker

С полным списком технологий можно ознакомиться в файле ```requirements.txt```
</details>

***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Шаблон наполнения env-файла</summary>

В проекте используется база данных PostgreSQL. Для взаимодействия с базой необходимо в директории ```foodgram-project-react/infra/``` создать файл ```.env``` по следующему шаблону.

```
SECRET_KEY=<project-secret-key>

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
</details>

***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Запуск проекта</summary>

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:GhoulNEC/foodgram-project-react.git
```

```
cd foodgram-project-react/infra/
```

Создать образ и запустить контейнер:

```
docker-compose up -d
```

Выполнить миграции:

```
docker-compose exec backend python manage.py migrate
```

Создать суперюзера:

```
docker-compose exec backend python manage.py createsuperuser
```

Собрать статику:

```
docker-compose exec backend python manage.py collectstatic --no-input
```

С документацией проекта можно ознакомиться по [ссылке](http://recipes-book.serveblog.net/api/docs/)

</details>

***

<details>
    <summary style="font-size: 16pt; font-weight: bold">Заполнение базы данных</summary>

Выполнить команду для заполнения базы данных из файла:

```
docker-compose exec backend python manage.py fill_db
```

</details>

***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Автор</summary>

[Роман Евстафьев](https://github.com/GhoulNEC)
</details>

***
