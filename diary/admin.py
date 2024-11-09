from django.contrib import admin
from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "is_public",
        "created_at",
    )  # Отображаемые колонки в списке
    list_filter = ("is_public", "created_at")  # Фильтры
    search_fields = ("title", "content", "author__email")  # Поля для поиска
    date_hierarchy = "created_at"  # Иерархия по датам
    ordering = ("-created_at",)  # Сортировка по умолчанию
    readonly_fields = ("created_at",)  # Поля только для чтения
    fieldsets = (
        (None, {"fields": ("title", "content", "author", "is_public", "image")}),
        (
            "Дополнительная информация",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),  # Скрытая секция
            },
        ),
    )
