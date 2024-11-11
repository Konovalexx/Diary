from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    avatar = forms.ImageField(required=False, label="Фото (необязательно)")
    phone_number = forms.CharField(required=False, label="Телефон (необязательно)")
    country = forms.CharField(required=False, label="Страна (необязательно)")

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2", "avatar", "phone_number", "country")

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("username")
        user = CustomUser.objects.filter(email=email).first()

        if user and not user.is_active:
            raise forms.ValidationError("Ваш аккаунт не активен. Подтвердите ваш email.")
        return cleaned_data