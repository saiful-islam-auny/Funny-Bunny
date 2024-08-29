from django import forms
from .models import Joke, Comment, Rating

class JokeForm(forms.ModelForm):
    class Meta:
        model = Joke
        fields = ['title', 'content', 'category']
    def __init__(self, *args, **kwargs):
        super(JokeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']
        widgets = {
            'stars': forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)]),
        }

