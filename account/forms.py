from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES, widget=forms.Select(), required=True)

    class Meta:
        model = CustomUser
        fields = ["user_name", "password1", "password2", "user_type"]