from django import forms
import logging

logger = logging.getLogger(__name__)



class SignForm(forms.Form):
    login = forms.CharField(label='login', max_length=100)
    password = forms.CharField(label='password', max_length=100)

    def get_login(self) -> str:
        return self.cleaned_data['login']

    def get_password(self) -> str:
        return self.cleaned_data['password']