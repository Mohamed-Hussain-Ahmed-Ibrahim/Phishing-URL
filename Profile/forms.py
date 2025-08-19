from django.contrib.auth.models import User
from django import forms


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    current_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
        current_password = cleaned_data.get('current_password')
        if new_password and not confirm_new_password:
            raise forms.ValidationError("You must confirm your new password.")
        if new_password != confirm_new_password:
            raise forms.ValidationError("Your new passwords do not match.")
        if not self.instance.check_password(current_password):
            raise forms.ValidationError("Your current password is incorrect.")
        return cleaned_data
