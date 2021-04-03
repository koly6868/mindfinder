from django import forms


class CreateChatForm(forms.Form):
    target_user_id = forms.IntegerField()

    def get_target_user_id(self):
        return self.cleaned_data['target_user_id']