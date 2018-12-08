from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User,History,ItemList


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email','age','sex','user_pic')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email','age','sex')

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ('height', 'weight', 'fat', 'push_pr', 'squat_pr', 'lift_pr','actlevel')


class MenuForm(forms.Form):
    def __init__(self, choice, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields['items'] = forms.MultipleChoiceField(choices=tuple([(name[0], name[1]) for name in choice]),label="菜單項目")
    items = forms.MultipleChoiceField()
