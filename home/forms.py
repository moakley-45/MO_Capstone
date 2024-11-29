from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'biography': 'Tell us about yourself...',
        }

        for field in self.fields:
            if field in placeholders:
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder