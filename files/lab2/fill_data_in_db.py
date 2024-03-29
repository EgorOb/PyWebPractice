"""
Заполнение данных в БД через скрипт python.
Для заполнения, достаточно просто запустить скрипт.

Так же приведенные команды в блоке (if __name__ == "__main__":)
можно аналогично выполнить в окружении запускаемом командой
python manage.py shell

В случае вызова консоли (python manage.py shell), то так же как и в
приведенном блоке (if __name__ == "__main__":) необходимо
импортировать модели с которыми будете работать и далее выполнять команды с БД.
"""

import os
from time import time
from datetime import date, datetime
import re
from json import load, dump

from django.core.exceptions import ValidationError
from django.core.files import File
from django.utils import timezone
from faker import Faker
from create_users import create_fake_users


# _____________Для работы с БД в Django через скрипт - этот блок обязателен !___
from django import setup
# Блок обязательно должен быть определен до импорта моделей БД
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  # Передача параметров в окружение
setup()  # Загрузка настроек Django
# ______________________________________________________________________________

from django.contrib.auth.models import User  # Загрузка базового пользователя
from apps.app.models import Blog, UserProfile, AuthorProfile, Entry, Tag, Comment

# _____________Чтение данных из json для добавления в БД________________________
with open("data/json_data/blogs.json", encoding="utf-8") as f:
    data_blog = load(f)
with open("data/json_data/users_profile.json", encoding="utf-8") as f:
    data_user_profile = load(f)
with open("data/json_data/authors_profile.json", encoding="utf-8") as f:
    data_author_profile = load(f)
with open("data/json_data/entrys.json", encoding="utf-8") as f:
    data_entry = load(f)
with open("data/json_data/tags.json", encoding="utf-8") as f:
    data_tag = load(f)
with open("data/json_data/comments.json", encoding="utf-8") as f:
    data_comment = load(f)
# ______________________________________________________________________________

if __name__ == "__main__":
    # _____________Создание пользователей_______________________________________
    # Создание администратора
    User.objects.create_superuser("admin", password="123")
    print("Админ создан \n    Логин: admin\n    Пароль: 123")

    # Работает долго, хеширование пароля занимает много времени
    create_fake_users(5, True)  # Создание аккаунта для персонала

    create_fake_users(35, False)  # Создание аккаунта для персонала

    print()  # Просто, чтобы сделать отступ в консоли

    # ______Работа с разрешениями_____________________________________

    from django.contrib.auth.models import Group, Permission

    # Получаем группу "Авторы"
    authors_group, created = Group.objects.get_or_create(name='Авторы')

    # Получаем разрешения, которые определены в модели Entry
    view_entry_permission = Permission.objects.get(codename='can_view_entry')
    add_entry_permission = Permission.objects.get(codename='can_add_entry')
    change_entry_permission = Permission.objects.get(codename='can_change_entry')
    delete_entry_permission = Permission.objects.get(codename='can_delete_entry')

    # Назначаем разрешения группе "Авторы"
    authors_group.permissions.add(
        view_entry_permission,
        add_entry_permission,
        change_entry_permission,
        delete_entry_permission
    )

    # Применение группы для пользователя
    for data in data_author_profile:
        user = User.objects.get(id=data["user_id"])
        user.groups.add(authors_group)

    print("Разрешения на Авторов созданы")

    # ______Работа с объектами таблицы Blog_____________________________________
    t_start = time()
    """Пример записи в БД с последующим сохранением"""
    obj = Blog(name=data_blog[0]["name"], slug_name=data_blog[0]["slug_name"],
               headline=data_blog[0]["headline"], description=data_blog[0]["description"])
    obj.save()

    """Пример записи в БД с сохранением (в нашем случае, так как работаем с словарём,
    то можно применить распаковку **)"""
    Blog.objects.create(**data_blog[1])

    """Никто не запрещает использовать циклы, минус в том, что при работе с циклами
    каждая запись сохраняется в БД по одному, что может создавать дополнительную
    нагрузку на БД"""
    for data in data_blog[2:]:
        Blog.objects.create(**data)

    result_time = time() - t_start
    print(f"Записи в таблицу Блог созданы, всего {len(data_blog)} записей. Время "
          f"выполнения: {result_time:.4f} c")

    # ______Работа с объектами таблицы AuthorProfile___________________________________
    """Если необходимо записать объекты пакетом, то для этих целей существует bulk_create,
    Однако он записывает данные в БД, если это контейнер подготовленных объектов
    к записи, а не сырые данные."""
    data_for_write = [AuthorProfile(user=User.objects.get(id=data["user_id"]),
                                    bio=data["bio"]) for data in data_author_profile[:10]] # Здесь
    # просто создались объекты, записи в БД не было
    AuthorProfile.objects.bulk_create(data_for_write)  # А здесь произошла пакетная запись в БД

    """
    При использовании Django ORM в Python - скрипте или через оболочку shell, 
    перед любым сохранением (save, create, bulk_create, bulk_update) в БД по 
    умолчанию Django не проводит проверку валидации! Это сделано по нескольким причинам:
    
    * Гибкость и Производительность: Django предоставляет разработчикам гибкость 
    в управлении когда и как выполняется валидация. Это особенно важно в сценариях, 
    где требуется высокая производительность, и каждый дополнительный шаг проверки 
    может существенно замедлить выполнение операций. Например, при массовом 
    создании или обновлении данных, дополнительные проверки могут сильно 
    увеличить время выполнения.
    
    * Контекст Зависимая Валидация: Не всегда все проверки, определённые на 
    уровне модели, актуальны. В некоторых ситуациях, в зависимости от контекста, 
    некоторые проверки могут быть ненужны или даже нежелательны.
    
    * Разделение Ответственности: Django следует принципу, что валидация данных - 
    это отдельная задача от сохранения данных. Это значит, что разработчик 
    должен ясно понимать, когда и где необходимо проводить валидацию, и делать 
    это явно. Это помогает предотвратить случайные ошибки и делает код более 
    читаемым и поддерживаемым.
    
    * Валидация на Уровне Формы: Во многих случаях валидация данных в Django 
    обычно происходит на уровне форм, а не моделей. В контексте веб-приложения, 
    данные часто проверяются при их вводе через формы, что является первой 
    линией защиты от невалидных данных.
    
    Однако возможно явно вызвать эти проверки и обработать
    возможные исключения, чтобы убедиться, что данные соответствуют заданным
    ограничениям полей для этого у объекта, который создали для записи необходимо
    вызвать метод full_clean(). За счёт доп. проверок общее время записи увеличится. 

    Для более наглядной части создадим функцию с проверкой
    """
    def check_obj_for_write_to_db(instance, save=True):
        try:
            instance.full_clean()  # Пытаемся провести проверки. Если где либо будет невалидное поле, то вызовется ошибка
        except ValidationError as e:
            fields = instance._meta.fields  # Получение
            # всех полей у объекта, необходимо чтобы вывести в трассировке
            # с какими параметрами был объект с ошибками. Выводит без полей с
            # отношениями с другими таблицами
            params = ""
            for field in fields:
                field_name = field.name
                field_value = getattr(instance, field_name)
                params += f"{field_name}={field_value!r}, "
            print(f"Ошибка при создании объекта: {e}\n"
                  f"Объект: {instance.__class__.__name__}({params[:-2]})")
        else:
            if save:
                instance.save()  # Объект успешно создан
            return True
        return False

    """Пример одиночной записи с проверкой, в случае удачных проверок - запишется,
    если нет, то появится ошибка, но выполнению кода это не помешает, так как
    был специально написан обработчик исключения в check_obj_for_write_to_db"""
    obj = AuthorProfile(user=User.objects.get(id=data_author_profile[10]["user_id"]),
                        bio=data_author_profile[10]["bio"])
    check_obj_for_write_to_db(obj)

    """Пример с ошибкой"""
    obj = AuthorProfile(user=User.objects.get(id=10))
    check_obj_for_write_to_db(obj)  #  Пытаемся записать пользователя который уже есть в БД
    """
    В консоль выведется
    Ошибка при создании объекта: {'user': ['Профиль автора with this User already exists.']}
    Объект: AuthorProfile(id=None, user=<User: valentinbelov>, bio=None, created_at=None, updated_at=None)
    """

    """
    К сожалению для AuthorProfile.objects.create(**data_author[10]) не получится провести
    встроенные проверки, так как внутри вызывается save() который делает базовые проверки.

    Для bulk_create аналогичная ситуация, однако можно провести проверки в момент
    формирования контейнера объектов для записи. Ниже приведён пример как можно
    это сделать. В рассматриваемом примере если существует хотя бы одна ошибка,
    то весь блок не записывается.
    """

    """Пример с ошибкой в блоке"""
    raw_data = data_author_profile[11:] + [{"user_id": 10, "bio": "bio"}]
    # Делаем фильтрацию, чтобы отсеить строки, что не прошли проверку
    data_for_write = list(filter(lambda x: check_obj_for_write_to_db(x, False),
                                 (AuthorProfile(user=User.objects.get(id=data["user_id"]),
                                                bio=data["bio"])
                                  for data in raw_data))
                          )
    # Проверяем на целостность, если данные были отсеян, то не записываем целый блок (имитация Атомарности из концепции acid)
    if len(data_for_write) == len(raw_data):
        AuthorProfile.objects.bulk_create(data_for_write)
    """
    В консоль выведется
    Ошибка при создании объекта: {'email': ['Enter a valid email address.']}
    Объект: Author(id=None, name='user1', email='user1')"""

    t_start = time()

    """Рабочий пример"""
    raw_data = data_author_profile[11:]
    data_for_write = list(
        filter(lambda x: check_obj_for_write_to_db(x, False),
               (AuthorProfile(user=User.objects.get(id=data["user_id"]),
                              bio=data["bio"]) for data in raw_data)
               ))

    if len(data_for_write) == len(raw_data):
        AuthorProfile.objects.bulk_create(data_for_write)

    result_time = time() - t_start
    print(
        f"\nЗаписи в таблицу AutorProfile созданы, всего {len(data_author_profile)} записей. Время "
        f"выполнения: {result_time:.4f} c")

    # ______ Работа с объектами таблицы UserProfile __________________________
    t_start = time()

    """Далее рассмотрим создание объектов с отношениями. Для того чтобы создать
    запись в БД в таблице где есть отношение, то в это поле необходимо передавать
    объект базы данных связанный с необходимым ключом(значением).

    """
    for data in data_user_profile:
        user = User.objects.get(id=data["user_id"])
        # Создаём автора с иконкой по умолчанию
        obj = UserProfile(user=user,
                          phone_number=data["phone_number"],
                          city=data["city"])

        check = check_obj_for_write_to_db(obj)

        """чтобы провести теже действия, что проводит Django при сохранении файла
        необходимо вызвать save от этого поля, это немного отличается от ранее
        рассмотренной валидации, так как тут рассматривается конкретное поле со своей спецификой
        """
        if check and data["avatar"] is not None:  # Если ошибок нет, и картинку нужно поменять (так как есть путь до
            # картинки), то запускаем протокол сохранения картинки
            with open(data["avatar"], 'rb') as file:  # Считываем картинку
                image_file = File(file)  # Создаём объект File
                obj.avatar.save(os.path.basename(data["avatar"]), image_file)  # Сохраняем картинку
                # (запускается механизм переноса картинки в хранилище)

    result_time = time() - t_start
    print(
        f"Записи в таблицу UserProfile созданы, всего {len(data_user_profile)} записей. Время "
        f"выполнения: {result_time:.4f} c")

    ## ______ Работа с объектами таблицы Tag ___________________________________
    t_start = time()

    for tag in data_tag:
        Tag.objects.create(**tag)

    result_time = time() - t_start
    print(
        f"Записи в таблицу Tag созданы, всего {len(data_tag)} записей. Время "
        f"выполнения: {result_time:.4f} c")

    ## ______ Работа с объектами таблицы Entry _________________________________
    t_start = time()

    blogs = Blog.objects.all()
    authors = AuthorProfile.objects.all()
    tags = Tag.objects.all()
    re_split = re.compile(r'[ :-]')
    for entry in data_entry:
        blog = blogs.get(name=entry["blog"])
        author = authors.filter(user__id__in=entry["authors_id"])
        tag = tags.filter(name__in=entry["tags"])
        # pub_date в моделях объявлен как DateTimeField, поэтому на вход необходимо подавать объект datetime
        pub_date = datetime(*map(int, re_split.split(entry["pub_date"]))) if \
            entry["pub_date"] is not None else datetime.now()
        pub_date = timezone.make_aware(pub_date)  # добавляем данных о часовом поясе, так как могут быть проблемы с БД и Django
        obj = Entry(blog=blog,
                    headline=entry["headline"],
                    slug_headline=entry["slug_headline"],
                    summary=entry["summary"],
                    body_text=entry["body_text"],
                    image=entry["image"],
                    pub_date=pub_date,
                    number_of_comments=entry["number_of_comments"],
                    number_of_pingbacks=entry["number_of_pingbacks"],
                    rating=entry["rating"] if entry["rating"] is not None else 0.0)

        check_obj_for_write_to_db(obj)
        obj.authors.set(author)  # Запись отношение многое ко многому немного специфичная
        # необходимо сначала сохранить в БД, а затем установить значения отношений
        obj.tags.set(tag)

    result_time = time() - t_start
    print(
        f"Записи в таблицу Entry созданы, всего {len(data_entry)} записей. Время "
        f"выполнения: {result_time:.4f} c")

    ## ______ Работа с объектами таблицы Comment _______________________________
    t_start = time()
    for comment in data_comment:
        entry = Entry.objects.get(headline=comment["entry"])
        user = User.objects.get(id=comment["user_id"])
        parent_id = comment.get("parent_id")
        Comment.objects.create(user=user, entry=entry, text=comment["text"],
                               parent=Comment.objects.get(
                                   id=parent_id) if parent_id else None)

    result_time = time() - t_start
    print(
        f"Записи в таблицу Comment созданы, всего {len(data_comment)} записей. Время "
        f"выполнения: {result_time:.4f} c")