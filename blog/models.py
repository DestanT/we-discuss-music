from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

User = get_user_model()

# Credit: CI 'Django Blog' walkthrough project
class Season(models.Model):
    '''
    Model for season blog posts.

    Attributes:
    - title (CharField)
    - slug (SlugField)
    - description (TextField)
    - image (CloudinaryField)
    - author (FK - User)
    - created_on (DateTimeField)
    '''
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=False)
    image = CloudinaryField(
        'image',
        default='placeholder',
        transformation=[{'width':1350, 'height':600, 'crop':'auto'}]
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='seasons')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Season Posts'

    def __str__(self):
        return self.title


class SpotifyPlaylist(models.Model):
    '''
    Model for Spotify playlists.

    Attributes:
    - playlist_id (PK - CharField)
    - seasons (ManyToManyField - Season)
    - image (URLField)
    - name (CharField)
    - external_url (URLField)
    - iframe_uri (CharField)
    '''
    playlist_id = models.CharField(max_length=100, primary_key=True)
    seasons = models.ManyToManyField(Season, blank=True, related_name='playlists')
    image = models.URLField(max_length=200)
    name = models.CharField(max_length=300)
    external_url = models.URLField(max_length=100)
    iframe_uri = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Spotify Playlists'


# Credit: CI 'Django Blog' walkthrough project
class Comment(models.Model):
    '''
    Model for Comments.

    Attributes:
    - season (FK - Season)
    - user (FK - User)
    - body (TextField)
    - created_on (DateTimeField)
    '''
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(blank=False, max_length=300)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.body


# Credit: CI 'Django Blog' walkthrough project
class CommentReply(models.Model):
    '''
    Model for Replies.

    Attributes:
    - comment (FK - Season)
    - user (FK - User)
    - body (TextField)
    - created_on (DateTimeField)
    '''
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField(blank=False, max_length=300)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']
        verbose_name_plural = 'Replies'

    def __str__(self):
        return self.body
