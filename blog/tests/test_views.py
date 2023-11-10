from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Season
from blog.views import *


class TestSeasonListView(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create(username='testUser')
        self.season = Season.objects.create(
            title='Test Title',
            slug='test-title',
            description='Some description',
            author=self.test_user,
            created_on='01-01-2023',
        )
        self.latest_season = Season.objects.create(
            title='Latest Season',
            slug='latest-season',
            description='This season was the last to be created',
            author=self.test_user,
            created_on='02-01-2023',
        )

    def test_season_list_view_status_code_is_200(self):
        response = self.client.get(reverse('homepage'))

        self.assertEqual(response.status_code, 200)

    def test_season_list_view_uses_correct_template(self):
        response = self.client.get(reverse('homepage'))

        self.assertTemplateUsed(response, 'index.html')

    def test_season_list_view_contains_all_season_objects(self):
        response = self.client.get(reverse('homepage'))
        list_length = len(response.context['object_list'])

        # Created 2 Season objects in setUp
        self.assertEqual(list_length, 2)

    def test_season_list_view_contains_latest_season_context(self):
        response = self.client.get(reverse('homepage'))
        latest_season = response.context['latest_season']

        self.assertEqual(latest_season, self.latest_season)



    # def test_season_detail_view_GET(self):
    #     pass

    # def test_season_create_view_POST(self):
    #     pass

    # def test_comment_create_view_POST(self):
    #     pass

    # def test_comment_update_view_POST(self):
    #     pass

    # def test_comment_delete_view_POST(self):
    #     pass

    # def test_reply_create_view_POST(self):
    #     pass

    # def test_spotify_api_form_view(self):
    #     pass