from django import forms
from .models import MyFormModel

class MyForm(forms.ModelForm):
    file = forms.FileField(required=True, label='File')

    class Meta:
        model = MyFormModel
        fields = ('file',)

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.txt'):
            raise forms.ValidationError('File must be a text file (.txt)')
        return file

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.file_url = self.cleaned_data['file'].name
        if commit:
            instance.save()
        return instance


