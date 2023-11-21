from django import forms
from django.forms import ModelForm, Textarea
from .models import Season, Comment, CommentReply


class SeasonForm(ModelForm):
    class Meta:
        model = Season
        fields = ('title', 'description', 'image')
        labels = {
            'title': 'Season Title',
            'description': 'Write a short description',
            'image': 'Add a cover image'
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {'body': ''}
        widgets = {
            'body': Textarea(attrs = {
                'cols': 40,
                'rows': 1,
                'placeholder': 'Add a comment...',
            }),
        }


class CommentReplyForm(ModelForm):
    class Meta:
        model = CommentReply
        fields = ('body',)
        labels = {'body': ''}
        widgets = {
            'body': Textarea(attrs = {
                'cols': 40,
                'rows': 1,
                'placeholder': 'Add a reply...',
            }),
        }


SEARCH_PARAMETERS = [
    ('album', 'Album'),
    ('playlist', 'Playlist'),
]


class SpotifyApiForm(forms.Form):
    search = forms.CharField()
    params = forms.MultipleChoiceField(
        required = True,
        widget = forms.CheckboxSelectMultiple,
        choices = SEARCH_PARAMETERS,
    )
