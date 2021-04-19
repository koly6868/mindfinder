from django import forms
from .models import MESSAGE_MAX_LEN


class CreateChatForm(forms.Form):
    profile_id = forms.IntegerField()

    def get_profile_id(self):
        return self.cleaned_data['profile_id']


class NewMessageForm(forms.Form):
    chat_id = forms.IntegerField()
    owner_id = forms.IntegerField()
    message = forms.CharField(max_length=MESSAGE_MAX_LEN,
                              widget=forms.TextInput(attrs={'placeholder': 'Введите сообщение'}))

    def get_chat_id(self):
        return self.cleaned_data['chat_id']

    def get_owner_id(self):
        return self.cleaned_data['owner_id']

    def get_message(self):
        return self.cleaned_data['message']
