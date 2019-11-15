from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'text goes here', 'rows': '4', 'cols': '50'}))

    class Meta:
        model = Comment
        fields = ['content']
