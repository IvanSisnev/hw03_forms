from django.contrib import admin

from .models import Post, Group


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Класс для кастомизации админки модели Роst.
    """

    list_display: tuple = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    # Интерфейс для выбора сообщества
    list_editable: tuple = ('group',)
    # Интерфейс для поиска по тексту постов
    search_fields: tuple = ('text',)
    # Фильтрация по дате
    list_filter: tuple = ('pub_date',)
    # Вывод строки в случае отсутствия данных в записи
    empty_value_display: str = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
    Класс для кастомизации админки модели Group.
    """

    list_display: tuple = (
        'pk',
        'title',
        'slug',
        'description',
    )
