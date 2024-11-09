from django.urls import path
from .views import (
    IndexView,
    MyDiaryView,
    EntryCreateView,
    EntryDeleteView,
    EntryUpdateView,
)

app_name = "diary"

urlpatterns = [
    path(
        "", IndexView.as_view(), name="index"
    ),  # Главная страница с публичными записями
    path(
        "my-diary/", MyDiaryView.as_view(), name="my_diary"
    ),  # Личный дневник пользователя
    path("new/", EntryCreateView.as_view(), name="new_entry"),  # Создание новой записи
    path(
        "<int:pk>/edit/", EntryUpdateView.as_view(), name="update_entry"
    ),  # Редактирование записи
    path(
        "<int:pk>/delete/", EntryDeleteView.as_view(), name="delete_entry"
    ),  # Удаление записи
]

# Обработчик для медиа-файлов
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
