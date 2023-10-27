from .models import Comment, CommentReply
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ('body',)