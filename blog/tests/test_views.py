from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Season, Comment, CommentReply
from blog.views import *


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create(username='testUser')
        self.staff_member = User.objects.create(username='staffMember', is_staff=True)
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
        self.comment = Comment.objects.create(
            season=self.season,
            user=self.test_user,
            body='Test comment'
        )
        self.reply = CommentReply.objects.create(
            comment=self.comment,
            user=self.test_user,
            body='Replying to test comment'
        )

    # Tests for SeasonListView:
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

    # Tests for SeasonDetailView:
    def test_season_detail_view_status_code_is_200(self):
        response = self.client.get(reverse('season_detail', args=[self.season.slug]))

        self.assertEqual(response.status_code, 200)

    def test_season_detail_view_uses_correct_template(self):
        response = self.client.get(reverse('season_detail', args=[self.season.slug]))

        self.assertTemplateUsed(response, 'blog/season_detail.html')

    def test_season_detail_view_contains_season_object(self):
        response = self.client.get(reverse('season_detail', args=[self.season.slug]))
        response2 = self.client.get(reverse('season_detail', args=[self.latest_season.slug]))

        self.assertEqual(response.context['season'], self.season)
        self.assertEqual(response2.context['season'], self.latest_season)

    def test_season_detail_view_contains_comments_in_season(self):
        response = self.client.get(reverse('season_detail', args=[self.season.slug]))
        comments = response.context['comments']

        self.assertQuerySetEqual(comments, Comment.objects.filter(season=self.season))
        self.assertEqual(len(comments), 1)

    def test_season_detail_view_contains_replies_to_comments(self):
        response = self.client.get(reverse('season_detail', args=[self.season.slug]))
        comments = response.context['comments']

        self.assertIn(self.reply, comments[0].replies.all())

    def test_season_detail_view_contains_comment_form(self):
        response = self.client.get(reverse('season_detail', args=[self.season.slug]))

        self.assertIsInstance(response.context['comment_form'], CommentForm)

    def test_season_detail_view_contains_reply_form(self):
        response = self.client.get(reverse('season_detail', args=[self.season.slug]))

        self.assertIsInstance(response.context['reply_form'], CommentReplyForm)

    # Tests for SeasonCreateView:
    def test_season_create_view_staff_member_is_required(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('create_season'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/login/?next=/season/create/')
    
    def test_season_create_view_status_code_is_200_when_staff_member_is_logged_in(self):
        self.client.force_login(self.staff_member)
        response = self.client.get(reverse('create_season'))

        self.assertEqual(response.status_code, 200)

    def test_season_create_view_uses_correct_template(self):
        self.client.force_login(self.staff_member)
        response = self.client.get(reverse('create_season'))

        self.assertTemplateUsed(response, 'blog/create_season.html')

    def test_season_create_view_creates_new_season_object(self):
        self.client.force_login(self.staff_member)
        form_data = {'title': 'New Season Object', 'description': 'Some description'}
        response = self.client.post(reverse('create_season'), data=form_data)

        # SetUp creates 2 seasons, +1 = 3
        self.assertEqual(Season.objects.count(), 3)

    def test_season_create_view_form_valid_method_sets_slug_and_author_correctly(self):
        self.client.force_login(self.staff_member)
        form_data = {'title': 'New Season Object', 'description': 'Some description'}
        self.client.post(reverse('create_season'), data=form_data)
        new_season = Season.objects.first()

        self.assertEqual(new_season.slug, 'new-season-object') # type: ignore
        self.assertEqual(new_season.author, self.staff_member) # type: ignore

    def test_season_create_view_get_success_url_method_successfully_redirects(self):
        self.client.force_login(self.staff_member)
        form_data = {'title': 'New Season Object', 'description': 'Some description'}
        response = self.client.post(reverse('create_season'), data=form_data)
        new_season = Season.objects.first()
        success_url = reverse('season_detail', kwargs={'slug': new_season.slug}) # type: ignore

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, success_url)


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