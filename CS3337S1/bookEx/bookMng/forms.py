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
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
            'price': forms.NumberInput(attrs={'class': 'form-control rounded-pill'}),
            'web': forms.URLInput(attrs={'class': 'form-control rounded-pill'}),
            'description': forms.Textarea(attrs={'class': 'form-control rounded-pill'}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Add your comment here...'}),
        }
