from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog.views import *


class TestUrls(SimpleTestCase):

    def test_homepage_url_resolves(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func.view_class, SeasonList)

    def test_create_season_url_resolves(self):
        url = reverse('create_season')
        self.assertEquals(resolve(url).func.view_class, SeasonCreateView)

    def test_season_detail_url_resolves(self):
        url = reverse('season_detail', args=['test-slug'])
        self.assertEquals(resolve(url).func.view_class, SeasonDetailView)

    def test_spotify_search_url_resolves(self):
        url = reverse('spotify_search', args=['test-slug'])
        self.assertEquals(resolve(url).func.view_class, SpotifyApiView)

    def test_season_comment_url_resolves(self):
        url = reverse('season_comment', args=['test-slug'])
        self.assertEquals(resolve(url).func.view_class, CommentCreateView)

    def test_comment_reply_url_resolves(self):
        url = reverse('comment_reply', args=['test-slug', '1'])
        self.assertEquals(resolve(url).func.view_class, ReplyCreateView)

    def test_update_comment_url_resolves(self):
        url = reverse('update_comment', args=['test-slug', '1'])
        self.assertEquals(resolve(url).func.view_class, CommentUpdateView)

    def test_delete_comment_url_resolves(self):
        url = reverse('delete_comment', args=['test-slug', '1'])
        self.assertEquals(resolve(url).func.view_class, CommentDeleteView)