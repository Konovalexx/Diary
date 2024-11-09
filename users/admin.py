from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "phone_number",
        "country",
        "email_verified",
    )  # Замените 'username' на 'email'
    search_fields = ("email", "phone_number")  # Замените 'username' на 'email'
    list_filter = ("email_verified", "country")
    readonly_fields = ("email_verification_token",)
