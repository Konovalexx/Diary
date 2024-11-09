from django.db import models
from django.conf import settings  # Импортируем settings


class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_public = models.BooleanField(default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # Используем кастомную модель
    image = models.ImageField(upload_to="entries/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
