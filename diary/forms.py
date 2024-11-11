from django import forms
from .models import Entry


# Форма для создания записи
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


# Форма для поиска
class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по заголовку или содержимому...'
        })
    )
    is_public = forms.BooleanField(
        required=False,
        label="Публичные записи",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    author = forms.CharField(
        max_length=100,
        required=False,
        label="Автор",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по автору...'
        })
    )

    def filter_entries(self, queryset):
        """Метод для фильтрации записей по параметрам формы"""
        query = self.cleaned_data.get('query')
        is_public = self.cleaned_data.get('is_public')
        author = self.cleaned_data.get('author')

        if query:
            queryset = queryset.filter(title__icontains=query) | queryset.filter(content__icontains=query)
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public)
        if author:
            queryset = queryset.filter(author__email__icontains=author)

        return queryset