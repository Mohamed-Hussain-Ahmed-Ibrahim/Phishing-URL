# forms.py
from django import forms
from django.db import models
from .models import Website
class MyForm(forms.Form):
    url = forms.URLField(max_length=10000)







class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['url']
