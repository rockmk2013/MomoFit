from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from .models import History

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email','age','sex')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email','age','sex')

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ('height', 'weight', 'fat', 'push_pr', 'squat_pr', 'lift_pr','actlevel')