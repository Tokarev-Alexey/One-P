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
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')
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
                         'font-size: 15px;'})}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            print(cd)
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


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
