from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES, widget=forms.Select(), required=True)

    class Meta:
        model = CustomUser
        fields = ["user_name", "password1", "password2", "user_type"]

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.user_type = self.cleaned_data["user_type"]
    #     user.user_name = self.cleaned_data["user_name"]
    #     if commit:
    #         user.save()
    #     return user