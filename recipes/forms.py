from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'notes', 'ingredients', 'method', 'serves', 'cuisine']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 5}),
            'method': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Recipe'))
