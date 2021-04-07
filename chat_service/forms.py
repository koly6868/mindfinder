from django import forms


class CreateChatForm(forms.Form):
    profile_id = forms.IntegerField()

    def get_profile_id(self):
        return self.cleaned_data['profile_id']