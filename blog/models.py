from django.db import models
from django.contrib.auth.models import User


class Season(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='seasons')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title