from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML
from .models import Recipe, Review, ReviewComment
from django_summernote.widgets import SummernoteWidget

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'notes', 'ingredients', 'method', 'serves', 'cuisine']
        widgets = {
            'notes': SummernoteWidget(attrs={'width': '100%'}),
            'ingredients': SummernoteWidget(attrs={'width': '100%'}),
            'method': SummernoteWidget(attrs={'width': '100%'}),
        }
        help_texts = {
            'title': 'Enter a descriptive title for your recipe!',
            'image': "Upload a clear image of your finished dish - we'd recommend a 1600 x 900px jpg, to ensure a good aspect ratio.",
            'notes': "Add any additional notes or tips about the recipe, or any interesting context about the recipe's creation!",
            'ingredients': "List all ingredients with their quantities - we'd recommend using the Unordered List option to better format this.",
            'method': "Provide step-by-step instructions for preparing the dish - we'd recommend using the Ordered List optoon to better format this.",
            'serves': 'Indicate how many people this recipe serves - please note, this field will only accept numbers.',
            'cuisine': "Select the type of cuisine this recipe belongs to - if you are unsure, leave this as 'Non-specific', as per the default.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            *[Field(field, template='recipes/custom_field.html') for field in self.fields]
        )
        self.helper.add_input(Submit('submit', 'Submit Recipe'))
 
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'image', 'content', 'rating')
        widgets = {
            'content': SummernoteWidget(attrs={'width': '100%'}),
        }
        help_texts = {
            'title': 'Enter a descriptive title for your review - sum up your thoughts with a snappy line!',
            'image': "Upload a clear image of your finished dish, if you'd like to - we'd recommend a 1600 x 900px jpg, to ensure a good aspect ratio.",
            'content': "Share your honest feelings about the recipe; how it tasted and what changes you'd recommend - please be constructive with your feedback though! Overly-personal attacks and insults will result in your Review not passing moderation. ",
            'rating': "Select your final rating for the recipe from 0 stars to 5 stars - if it was an awful meal, give it zero! If you can't wait to make it again, give it five!",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('title', wrapper_class='mb-2'),
            HTML('<div class="help-text mb-2">{{ form.title.help_text }}</div>'),
            Field('image', wrapper_class='mb-2'),
            HTML('<div class="help-text mb-2">{{ form.image.help_text }}</div>'),
            Field('content', wrapper_class='mb-2'),
            HTML('<div class="help-text mb-2">{{ form.content.help_text }}</div>'),
            Field('rating', wrapper_class='mb-2'),
            HTML('<div class="help-text mb-2">{{ form.rating.help_text }}</div>'),
        )
        self.helper.add_input(Submit('submit', 'Submit Review', id='reviewSubmitButton'))


class ReviewCommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add your comment here...'}), label='')

    class Meta:
        model = ReviewComment
        fields = ('body',)
