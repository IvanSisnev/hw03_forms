from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
    Класс для создания формы новой записи.
    """
    class Meta:
        model = Post
        fields = ('text', 'group')
