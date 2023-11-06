from django.test import TestCase
from blog.forms import SeasonForm
from blog.models import Season


class TestSeasonForm(TestCase):

    def test_season_title_is_required(self):
        form = SeasonForm({'title': '', 'description': 'anything'})

        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertEqual(form.errors['title'][0], 'This field is required.')

    def test_season_description_is_required(self):
        form = SeasonForm({'title': 'anything', 'description': ''})

        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors.keys())
        self.assertEqual(form.errors['description'][0], 'This field is required.')

    def test_season_title_is_unique(self):
        Season.objects.create(title = 'The same title', slug = 'the-same-title', description = 'anything')
        form = SeasonForm({'title': 'The same title', 'slug': 'the-same-title', 'description': 'anything'})
        
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertEqual(form.errors['title'][0], 'Season with this Title already exists.')

    def test_season_form_is_valid(self):
        form = SeasonForm({'title': 'New Season', 'slug': 'new-season', 'description': 'Some description'})

        self.assertTrue(form.is_valid())

    def test_season_form_is_invalid(self):
        form = SeasonForm({})

        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertIn('description', form.errors.keys())

    def test_fields_are_explicit_in_form_metaclass(self):
        form = SeasonForm()
        
        self.assertEqual(form.Meta.fields, ('title', 'description', 'image'))