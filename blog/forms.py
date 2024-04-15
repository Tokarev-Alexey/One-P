from django import forms
from django.forms import TextInput, Textarea

from .models import Post, Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)
        widgets = {
            'title': TextInput(attrs={
                'style': 'width: 100%;'
                         'padding: 5px;'
                         'border-radius: 10px;'
                         'background-color: #333;'
                         'color: #ccc;'
                         'font-size: 15px;',
                'placeholder': 'Title',
            }),
            'text': Textarea(attrs={
                'style': 'width: 100%;'
                         'padding: 5px;'
                         'margin: 10px 0px 10px 0px;'
                         'border-radius: 10px;'
                         'background-color: #333;'
                         'color: #ccc;'
                         'font-size: 15px;',
                'placeholder': 'Text',
            })
        }


class UserRegistrationForm(forms.ModelForm):
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': TextInput(attrs={
                'style': 'width: 100%;'
                         'display: flex;'
                         'flex-direction: column;'
                         'align-items:center;'
                         'padding: 5px;'
                         'margin: 5px 0px 5px 0px;'
                         'border-radius: 10px;'
                         'background-color: #333;'
                         'color: #ccc;'
                         'font-size: 15px;'}),
        }

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            self.add_error('password2', 'Пароли не совпадают.')
        else:
            return password2


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': Textarea(attrs={
                'class': 'form-text',
                'style': 'width: 100%;'
                         'padding: 5px;'
                         'margin: 10px 0px 10px 0px;'
                         'border-radius: 10px;'
                         'background-color: #333;'
                         'color: #ccc;'
                         'font-size: 15px;',
                'placeholder': 'Add a new comment...'
            })
        }
