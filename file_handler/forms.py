from django import forms

from .models import FileHolder


class ImportForm(forms.ModelForm):

    class Meta:
        model = FileHolder
        fields = '__all__'
