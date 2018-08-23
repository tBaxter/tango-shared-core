import unittest

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.http import HttpRequest
from django.template import Template, Context, RequestContext
from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse
from django.views.generic import TemplateView

from .utils.sanetize import clean_text


class DummyModel(models.Model):
    """
    Dummy model for testing below
    """
    def get_absolute_url(self):
        return '/'


class TestSharedContent(TestCase):

    def setUp(self):
        self.slug = 'admin'

    def test_template_media(self):
        """
        Ensures base template has required media files.
        """
        response = self.client.get(reverse('home'))
        static_url = settings.STATIC_URL
        favicon_url = '<link rel="shortcut icon" href="{}img/favicon.png">'.format(static_url)
        touch_icon = '<link rel="apple-touch-icon" href="{}img/touch-icon.png">'.format(static_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('STATIC_URL' in response.context_data)
        self.assertTrue(favicon_url in response.rendered_content)
        self.assertTrue(touch_icon in response.rendered_content)

    def test_page_resolution(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'page for testing')

    def test_shared_context_processor(self):
        """
        Test results of shared context processor are in template
        """
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'site')
        self.assertTrue('now' in response.context)
        self.assertTrue('current_path' in response.context)
        self.assertTrue('last_seen' in response.context)
        self.assertTrue('last_seen_fuzzy' in response.context)
        self.assertTrue('theme' in response.context)
        self.assertTrue('authenticated_request' in response.context)
        # These shouldn't be set, based on test setttings:
        self.assertTrue('project_name' in response.context)
        self.assertEqual(response.context['project_name'], None)

    def test_project_name(self):
        with self.settings(PROJECT_NAME='abc123'):
            response = self.client.get(reverse('home'))
            self.assertTrue('project_name' in response.context)
            self.assertTrue(response.context['project_name'], 'abc123')


class TemplateTagsTests(TestCase):
    def setUp(self):
        self.test_list = ['apples', 'oranges']
        self.factory = RequestFactory()

    def test_humanized_join(self):
        t = Template('{% load formatting %}{{ mylist|humanized_join }}')

        # with one item
        c = Context({"mylist": ['foo']})
        output = t.render(c)
        self.assertEqual(output, 'foo')

        # with two items
        c = Context({"mylist": self.test_list})
        output = t.render(c)
        self.assertEqual(output, 'apples and oranges')

        # with three
        self.test_list.append('pears')
        c = Context({"mylist": self.test_list})
        output = t.render(c)
        self.assertEqual(output, 'apples, oranges, and pears')

    @unittest.skip("Struggling to get request object in context processor")
    def test_social_links(self):
        t = Template('{% load social_tags %}{% social_links object %}')
        obj = DummyModel.objects.create()
        request = self.factory
        request.user = AnonymousUser()
        c = RequestContext(request, {"object": obj})
        output = t.render(c)
        self.assertTrue('facebook' in output)
        self.assertTrue('twitter' in output)


class UtilsTests(TestCase):
    def setUp(self):
        self.profanities = [
            ('what the fuck', 'what the smurf'),
            ('what the FUCK', 'what the SMURF'),
            ('what the Fuck', 'what the Smurf'),
            ('we are fucked', 'we are smurfed'),
            ('what a fucker', 'what a smurfer'),
            ('what a Fucker', 'what a Smurfer'),
            ('fucking guy',   'smurfing guy'),
            ('Fucking guy',   'Smurfing guy'),
        ]

    def test_profanity_replacement(self):
        for p in self.profanities:
            self.assertEqual(clean_text(p[0]), p[1])
