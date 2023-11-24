from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Season, Comment, CommentReply


class TestModels(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='testUser')

    def test_season_title_must_be_unique(self):
        Season.objects.create(
            title='The Same Title',
            slug='test',
            description='Test description',
            author=self.test_user,
            created_on='01-01-2023',
        )

        # Try to make another object with the same title.
        with self.assertRaises(Exception):
            Season.objects.create(
            title='The Same Title',
            slug='test',
            description='Test description',
            author=self.test_user,
            created_on='01-01-2023',
            )

    def test_season_model_str_method_returns_title(self):
        season = Season.objects.create(
            title='Test Title',
            slug='test',
            description='Test description',
            author=self.test_user,
            created_on='01-01-2023',
        )

        self.assertEqual(season.__str__(), season.title)

    def test_comment_model_str_method_returns_body(self):
        season = Season.objects.create(
            title='Test Title',
            slug='test',
            description='Test description',
            author=self.test_user,
            created_on='01-01-2023',
        )
        comment = Comment.objects.create(
            season=season,
            user=self.test_user,
            body='Test Body Content'
        )

        self.assertEqual(comment.__str__(), comment.body)

    def test_comment_reply_model_str_method_returns_body(self):
        season = Season.objects.create(
            title='Test Title',
            slug='test',
            description='Test description',
            author=self.test_user,
            created_on='01-01-2023',
        )
        comment = Comment.objects.create(
            season=season,
            user=self.test_user,
            body='Test Body Content'
        )
        reply = CommentReply.objects.create(
            comment=comment,
            user=self.test_user,
            body='Test Reply Body Content'
        )

        self.assertEqual(reply.__str__(), reply.body)