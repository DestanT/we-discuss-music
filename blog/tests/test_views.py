from django.test import TestCase, Client
from django.urls import reverse
from blog.models import *
from blog.views import *


class TestViews(TestCase):

    def test_season_list_view_GET(self):
        client = Client()
        response = client.get(reverse('homepage'))
        print(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_season_detail_view_GET(self):
        pass

    def test_season_create_view_POST(self):
        pass

    def test_comment_create_view_POST(self):
        pass

    def test_comment_update_view_POST(self):
        pass

    def test_comment_delete_view_POST(self):
        pass

    def test_reply_create_view_POST(self):
        pass

    def test_spotify_api_form_view(self):
        pass