from django.test import TestCase
from django.forms import Textarea
from blog.forms import SeasonForm, CommentForm, CommentReplyForm, SpotifyApiForm
from blog.models import Season


class TestSeasonForm(TestCase):

    def test_season_title_is_required(self):
        form = SeasonForm({
            'title': '',
            'description': 'anything'
            })

        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertEqual(form.errors['title'][0], 'This field is required.')

    def test_season_description_is_required(self):
        form = SeasonForm({
            'title': 'anything',
            'description': ''
            })

        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors.keys())
        self.assertEqual(form.errors['description'][0], 'This field is required.')

    def test_season_title_is_unique(self):
        # Create object
        Season.objects.create(
            title='The same title',
            slug='the-same-title',
            description='anything'
        )
        # Fill form with the same 'title' as object created
        form = SeasonForm({
            'title': 'The same title',
            'slug': 'the-same-title',
            'description': 'something'
            })

        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertEqual(form.errors['title'][0], 'Season with this Title already exists.')

    def test_season_form_is_valid(self):
        form = SeasonForm({
            'title': 'New Season',
            'slug': 'new-season',
            'description': 'Some description'
            })

        self.assertTrue(form.is_valid())

    def test_season_form_is_invalid(self):
        form = SeasonForm({})

        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertIn('description', form.errors.keys())

    def test_season_form_fields_are_explicit_in_form_metaclass(self):
        form = SeasonForm()

        self.assertEqual(form.Meta.fields, ('title', 'description', 'image'))

    def test_season_form_labels_display_correctly(self):
        form = SeasonForm()

        self.assertEqual(form.Meta.labels['title'], 'Season Title')
        self.assertEqual(form.Meta.labels['description'], 'Write a short description')
        self.assertEqual(form.Meta.labels['image'], 'Add a cover image')


class TestCommentForm(TestCase):

    def test_comment_body_is_required(self):
        form = CommentForm({'body': ''})

        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors.keys())
        self.assertEqual(form.errors['body'][0], 'This field is required.')

    def test_comment_form_is_valid(self):
        form = CommentForm({'body': 'Some comment'})

        self.assertTrue(form.is_valid())

    def test_comment_form_body_when_larger_than_300_characters(self):
        form = CommentForm({'body': 'x' * 301})

        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors.keys())
        self.assertEqual(
            form.errors['body'][0],
            'Ensure this value has at most 300 characters (it has 301).'
        )

    def test_comment_form_fields_are_explicit_in_form_metaclass(self):
        form = CommentForm()

        self.assertEqual(form.Meta.fields, ('body',))

    def test_comment_form_labels_display_correctly(self):
        form = CommentForm()

        self.assertEqual(form.Meta.labels['body'], '')

    def test_comment_form_widgets_are_set_correctly(self):
        form = CommentForm()

        self.assertIsInstance(form.Meta.widgets['body'], Textarea)
        self.assertEqual(
            form.Meta.widgets['body'].attrs,
            {'cols': 40, 'rows': 1, 'placeholder': 'Add a comment...',}
        )


class TestCommentReplyForm(TestCase):
    '''
    Tests are identical to TestCommentForm
    '''

    def test_reply_body_is_required(self):
        form = CommentReplyForm({'body': ''})

        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors.keys())
        self.assertEqual(form.errors['body'][0], 'This field is required.')

    def test_reply_form_is_valid(self):
        form = CommentReplyForm({'body': 'Some comment'})

        self.assertTrue(form.is_valid())

    def test_reply_form_body_when_larger_than_300_characters(self):
        form = CommentReplyForm({'body': 'x' * 301})

        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors.keys())
        self.assertEqual(
            form.errors['body'][0],
            'Ensure this value has at most 300 characters (it has 301).'
        )

    def test_reply_form_fields_are_explicit_in_form_metaclass(self):
        form = CommentReplyForm()

        self.assertEqual(form.Meta.fields, ('body',))

    def test_reply_form_labels_display_correctly(self):
        form = CommentReplyForm()

        self.assertEqual(form.Meta.labels['body'], '')

    def test_reply_form_widgets_are_set_correctly(self):
        form = CommentReplyForm()

        self.assertIsInstance(form.Meta.widgets['body'], Textarea)
        self.assertEqual(
            form.Meta.widgets['body'].attrs,
            {'cols': 40, 'rows': 1, 'placeholder': 'Add a reply...',}
        )


class TestSpotifyApiForm(TestCase):

    def test_search_field_is_required(self):
        form = SpotifyApiForm({'search': ''})

        self.assertFalse(form.is_valid())
        self.assertIn('search', form.errors.keys())
        self.assertEqual(form.errors['search'][0], 'This field is required.')

    def test_params_field_is_required(self):
        form = SpotifyApiForm({'search': 'Some search'})

        self.assertFalse(form.is_valid())
        self.assertIn('params', form.errors.keys())
        self.assertEqual(form.errors['params'][0], 'This field is required.')

    def test_form_is_valid_with_one_param_selected(self):
        param1 = ['album']
        form1 = SpotifyApiForm({'search': 'Some search', 'params': param1})
        param2 = ['playlist']
        form2 = SpotifyApiForm({'search': 'Some search', 'params': param2})

        self.assertTrue(form1.is_valid())
        self.assertTrue(form2.is_valid())

    def test_form_is_valid_with_both_params_selected(self):
        both_params = ['album', 'playlist']
        form1 = SpotifyApiForm({'search': 'Some search', 'params': both_params})
        reversed_params = ['playlist', 'album']
        form2 = SpotifyApiForm({'search': 'Some search', 'params': reversed_params})

        self.assertTrue(form1.is_valid())
        self.assertTrue(form2.is_valid())
