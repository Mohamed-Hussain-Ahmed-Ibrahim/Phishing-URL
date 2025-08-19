from django import forms

class MyForm(forms.Form):
    url = forms.URLField(max_length=200)