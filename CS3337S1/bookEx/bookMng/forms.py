from django import forms
from django.forms import ModelForm
from .models import Book
from .models import Comment



class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your comment here...', 'rows': 4}),
        }