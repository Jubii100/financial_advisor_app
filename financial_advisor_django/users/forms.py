from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile

auth_user = get_user_model()


class UserModelForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'name',
            'interests',
            'hobbies',
            'age',
            'gender',
            'net_worth',
        ]


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password"
            }
        )
    )

    class Meta:
        model = auth_user
        fields = [
            'username',
            'password',
        ]
