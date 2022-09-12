from django.forms import ModelForm
from django import forms
from organisations.models import Csv

class UploadForm(ModelForm):
    name = forms.TextInput()
    file = forms.FileField()
    class Meta:
        model = Csv
        fields = ['name','file']