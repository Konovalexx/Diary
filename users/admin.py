from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_number", "country", "is_active")  # Используем is_active вместо email_verified
    search_fields = ("email", "phone_number")
    list_filter = ("is_active", "country")  # Фильтрация по is_active
    readonly_fields = ("email_verification_token", "email_verified")  # email_verified только для чтения