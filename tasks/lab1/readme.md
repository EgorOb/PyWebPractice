
Создадим миграции

```python
python manage.py makemigrations
```

Создадим таблицы в базе данных (БД)
```python
python manage.py migrate
```

Загрузим данные через фикстуру (слепок данных БД)
```python
python manage.py loaddata data_db.json
```

Запустим сервер
```python
python manage.py runserver
```
