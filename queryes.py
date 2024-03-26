import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from apps.db_train_alternative.models import Blog, Author, AuthorProfile, Entry, Tag

    # TODO Сделайте здесь запросы

    # obj = Entry.objects.filter(author__name__contains='author')
    # print(obj)

    from django.db.models import Subquery

    # Получаем список ID авторов без биографии
    subquery = AuthorProfile.objects.filter(bio__isnull=True).values('author_id')

    # Фильтруем записи блога по авторам
    print(Entry.objects.filter(author__authorprofile__bio__isnull=True))












