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
                'class': 'form-title',
                'style': 'max-width: 600px;',
                'placeholder': 'Title',
            }),
            'text': Textarea(attrs={
                'class': 'form-text',
                'style': 'max-width: 600px;',
                'placeholder': 'Text',
            })
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': Textarea(attrs={
                'class': 'form-text',
                'style': 'width: 620px; height: 100px;',
                'placeholder': 'Add a new comment...',
            })
        }
