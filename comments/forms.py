
from django import forms
from . import models

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={'class': 'form-control', 'rows':'3'}
        )
    )

    class Meta:
        model = models.Comment
        fields = ['text']











