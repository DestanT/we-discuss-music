from .models import Season, Comment, CommentReply
from django.forms import ModelForm, Textarea


class SeasonForm(ModelForm):
    class Meta:
        model = Season
        fields = ('title', 'description', 'image')
        labels = {'title': 'Season Title', 'description': 'Write a short description', 'image': 'Add a cover image'}


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {'body': ''}
        widgets = {
            'body': Textarea(attrs={
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
            'body': Textarea(attrs={
                'rows': 1,
                'placeholder': 'Add a reply...',
            }),
        }