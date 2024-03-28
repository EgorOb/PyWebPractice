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

    filtered_data = Blog.objects.filter(id__gte=2).order_by("id")
    print(filtered_data)  # упорядочивание по возрастанию по полю id
    """
    <QuerySet [
    <Blog: Кулинарные искушения>, 
    <Blog: Фитнес и здоровый образ жизни>, 
    <Blog: ИТ-новости и технологии>, 
    <Blog: Мода и стиль>
    ]>
    """
    print(filtered_data.reverse())  # поменяли направление
    """
    <QuerySet [
    <Blog: Мода и стиль>, 
    <Blog: ИТ-новости и технологии>, 
    <Blog: Фитнес и здоровый образ жизни>, 
    <Blog: Кулинарные искушения>
    ]>
    """
    filtered_data = Blog.objects.filter(
        id__gte=2)  # Если порядок не указан или в модели, или через order_by, то reverse работать не будет
    print(filtered_data)
    print(filtered_data.reverse())












