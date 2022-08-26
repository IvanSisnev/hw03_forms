"""
Модуль для создания классов моделей.
"""

from django.contrib.auth import get_user_model
from django.db import models

from django.urls import reverse

User = get_user_model()


class Post(models.Model):
    """
    Класс модели Post для создания и редактирования записей.
    """

    date_format = "j E Y"
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')
    group = models.ForeignKey('Group', on_delete=models.SET_NULL,
                              related_name='posts', blank=True, null=True)

    class Meta:
        """
        Мета класс для сортировки.
        """
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Group(models.Model):
    """
    Класс модели Group для создания и редактирования сообществ.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        """
        Вернуть стоку с наименованием сообщества.
        """
        return self.title

    def get_absolute_url(self):
        """
        Cоздать URL адрес
        """
        return reverse('group_list', args=self.slug)
