import sqlite3
from datetime import datetime

# Подключение к базе данных SQLite
conn = sqlite3.connect('db_blog.sqlite3')
cursor = conn.cursor()

# Заполнение таблицы Blog
cursor.execute("INSERT INTO blog_blog (name, tagline) VALUES (?, ?)", ('Пример блога', 'Просто пример блога'))
blog_id = cursor.lastrowid

# Заполнение таблицы Author
cursor.execute("INSERT INTO blog_author (name, email) VALUES (?, ?)", ('Иван Иванов', 'ivan@example.com'))
author_id = cursor.lastrowid

# Заполнение таблицы AuthorProfile
cursor.execute("INSERT INTO blog_authorprofile (author_id, bio, phone_number, city) VALUES (?, ?, ?, ?)", (author_id, 'Lorem ipsum dolor sit amet', '+79123456789', 'Москва'))

# Заполнение таблицы Entry
cursor.execute("INSERT INTO blog_entry (blog_id, headline, body_text, pub_date, mod_date, author_id, number_of_comments, number_of_pingbacks, rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (blog_id, 'Первая запись', 'Это первая запись', datetime.now(), datetime.now(), author_id, 0, 0, 0.0))

# Заполнение таблицы Tag
cursor.execute("INSERT INTO blog_tag (name, slug_name) VALUES (?, ?)", ('Пример тега', 'primer-tega'))

# Получение идентификаторов вставленных строк
entry_id = cursor.lastrowid
tag_id = cursor.lastrowid

# Заполнение таблицы для связи многие-ко-многим между Entry и Tag
cursor.execute("INSERT INTO blog_entry_tags (entry_id, tag_id) VALUES (?, ?)", (entry_id, tag_id))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()