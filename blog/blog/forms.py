from django import forms

from blogapp.models import blog


class ModelForm(forms.ModelForm):
    class Meta:
        model=blog
        fields=['topic','title','img','desc']