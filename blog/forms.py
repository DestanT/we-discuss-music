from .models import Comment, CommentReply
from django.forms import ModelForm, Textarea


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