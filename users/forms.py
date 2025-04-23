from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm
from users.models import User


class UserCreationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=15,
        required=False,
        help_text='Введите номер телефона (необязательно)')

    country = forms.CharField(
        max_length=50,
        required=False,
        help_text='Введите страну (необязательно)')

    avatar = forms.ImageField(
        required=False,
        help_text='Загрузите аватар (необязательно)')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'email', 'phone', 'avatar', 'country', 'password1', 'password2')


class UserUpdateForm(ModelForm):
    password = None

    class Meta(UserChangeForm):
        model = User
        fields = ('phone', 'country', 'avatar')
