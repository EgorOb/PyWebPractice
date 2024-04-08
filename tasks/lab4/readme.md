

Но в DRF есть класс `DefaultRouter` из `rest_framework.routers` который прописывает пути по шаблону самостоятельно, им и воспользуемся.

В `urls.py` приложения `api` пропишите:

```python
from rest_framework.routers import DefaultRouter
from .views import AuthorAPIView

# Создание экземпляра DefaultRouter
router = DefaultRouter()

# Регистрация представления AuthorAPIView с именем 'authors'
router.register(r'authors', AuthorAPIView, basename='author')
```

В этом коде:

* Создается экземпляр класса `DefaultRouter`.
* Представление `AuthorAPIView` регистрируется в роутере под именем `'authors'`.

В роутере маршруты автоматически создадутся для каждого метода представления `AuthorAPIView` (GET, POST, PUT, PATCH, DELETE) 
и будут доступны по URL `/authors/` для списка авторов и `/authors/<pk>/` для конкретного автора, где <pk> - это первичный ключ автора.

В Django REST Framework, когда вы используете `router.register()` для регистрации представления в роутере, 
параметр `basename` определяет базовое имя для создаваемых URL. Это базовое имя используется при генерации именованных URL в представлениях, связанных с роутером.
В общем случае это что-то похоже, что ранее передавалось в параметр `name` в `path`

Вот как это работает:

Каждое представление, зарегистрированное в роутере, получает три именованных URL: 
* `<basename>-list`, 
* `<basename>-detail`, 
* `<basename>-set`. 

Например, если вы укажете `basename='author'`, то URL для списка объектов будет иметь имя `author-list`, для конкретного объекта - `author-detail`, а для набора - `author-set`.
Эти имена можно использовать в методах reverse() или reverse_lazy() для генерации URL внутри вашего кода.

Последнее, что осталось сделать, это зарегистрировать сам роутер для приложения `api`.

Для этого в `urls.py` папки `project` пропишем

```python
from apps.api.urls import router

urlpatterns = [
    # ...
    path('api/', include(router.urls)), 
]
```