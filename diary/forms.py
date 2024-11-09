from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["title", "content", "is_public", "image"]  # Добавляем поле 'image'
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите заголовок"}
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Введите содержание"}
            ),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control-file"}
            ),  # Добавляем виджет для поля изображения
        }
        labels = {
            "title": "Заголовок",
            "content": "Содержание",
            "is_public": "Публичная запись",
            "image": "Изображение",  # Заголовок для поля изображения
        }
