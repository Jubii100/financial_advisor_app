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
    # def __init__(self, *args, **kwargs):
    #     super(CaseForm, self).__init__(*args, **kwargs)

    # username = forms.CharField()
    # email = forms.EmailField()
    # password1 = forms.CharField(
    #     label='Password',
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control",
    #             "id": "user-password"
    #         }
    #     )
    # )
    # password2 = forms.CharField(
    #     label='Confirm Password',
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control",
    #             "id": "user-confirm-password"
    #         }
    #     )
    # )

    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     qs = auth_user.objects.filter(username__iexact=username)
    #     if username in non_allowed_usernames:
    #         raise forms.ValidationError(
    #             "This is an invalid username, please pick another.")
    #     if qs.exists():
    #         raise forms.ValidationError(
    #             "This is an invalid username, please pick another.")
    #     return username

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     qs = auth_user.objects.filter(email__iexact=email)
    #     if qs.exists():
    #         raise forms.ValidationError("This email is already in use.")
    #     return email
