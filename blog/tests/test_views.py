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
            author=self.staff_member,
            created_on='01-01-2023',
        )
        self.latest_season = Season.objects.create(
            title='Latest Season',
            slug='latest-season',
            description='This season was the last to be created',
            author=self.staff_member,
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

        self.assertTemplateUsed(response, 'blog/season_form.html')

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

    # Tests for SeasonUpdateView:
    def test_season_update_view_correctly_updates_object(self):
        self.client.force_login(self.staff_member)
        get_response = self.client.get(reverse('update_season', args=[self.season.slug]))

        # Get original Season object and check original title
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(self.season.title, 'Test Title')
        
        # Post updated form and check redirect
        form_data = {'title': 'Updated Title', 'description': 'Updated description'}
        post_response = self.client.post(reverse('update_season', args=[self.season.slug]), data=form_data)
        self.assertEqual(post_response.status_code, 302)

        # Check if slug and title changed correctly
        updated_season = Season.objects.get(slug='updated-title')
        self.assertEqual(updated_season.title, 'Updated Title')

    # Tests for SeasonDeleteView:
    def test_season_delete_view_successfully_deletes_object(self):
        self.client.force_login(self.staff_member)
        response = self.client.post(reverse('delete_season', args=[self.season.slug]))

        self.assertEqual(response.status_code, 302)

        # Try to retrieve deleted object
        get_response = self.client.get(reverse('season_detail', args=[self.season.slug]))

        self.assertEqual(get_response.status_code, 404)

    # Tests for CommentCreateView:
    def test_comment_create_view_creates_new_comment_object(self):
        self.client.force_login(self.staff_member)
        form_data = {'season': self.season, 'user': self.staff_member, 'body': 'This is a new comment'}
        previous_comment_count = Comment.objects.all().count()
        response = self.client.post(reverse('season_comment', args=[self.season.slug]), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.all().count(), previous_comment_count + 1)

    def test_comment_create_view_form_valid_method_sets_season_and_user_correctly(self):
        self.client.force_login(self.staff_member)
        form_data = {'season': self.season, 'user': self.staff_member, 'body': 'This is a test'}
        self.client.post(reverse('season_comment', args=[self.season.slug]), data=form_data)
        new_comment = Comment.objects.last()

        self.assertEqual(new_comment.user, self.staff_member) # type: ignore
        self.assertEqual(new_comment.season, self.season) # type: ignore

    def test_comment_create_view_get_success_url_method_successfully_redirects(self):
        self.client.force_login(self.staff_member)
        form_data = {'season': self.season, 'user': self.staff_member, 'body': 'This is a test'}
        response = self.client.post(reverse('season_comment', args=[self.season.slug]), data=form_data)
        success_url = reverse('season_detail', kwargs={'slug': self.season.slug}) # type: ignore

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, success_url)

    # Tests for CommentUpdateView:
    def test_comment_update_view_correctly_updates_object(self):
        self.client.force_login(self.staff_member)
        
        # Current comment
        self.assertEqual(self.comment.body, 'Test comment')
        self.assertEqual(self.comment.pk, 1)
        
        # Post updated form and check redirect
        form_data = {'body': 'Updated Comment'}
        post_response = self.client.post(reverse('update_comment', kwargs={'slug': self.season.slug, 'pk': self.comment.pk}), data=form_data)
        self.assertEqual(post_response.status_code, 302)

        # Check if slug and title changed correctly
        updated_comment = Comment.objects.get(pk=1)
        self.assertEqual(updated_comment.body, 'Updated Comment')

    # def test_comment_delete_view_POST(self):
    #     pass

    # def test_reply_create_view_POST(self):
    #     pass

    # def test_spotify_api_form_view(self):
    #     pass