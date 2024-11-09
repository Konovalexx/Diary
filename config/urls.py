from django.contrib import admin
from django.urls import path, include
from diary.views import IndexView  # Импортируем правильный класс представления
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='home'),  # Путь для главной страницы
    path('admin/', admin.site.urls),  # URL для административной панели
    path('diary/', include('diary.urls', namespace='diary')),  # URL для приложения diary
    path('users/', include('users.urls', namespace='users')),  # URL для приложения users
]

# Добавьте обработку медиа-файлов в случае, если DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)