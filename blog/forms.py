from django import forms
from django.forms import TextInput,Textarea
from .models import Post


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