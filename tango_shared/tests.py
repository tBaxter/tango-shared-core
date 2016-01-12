import unittest

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpRequest
from django.template import Template, Context, RequestContext
from django.test import TestCase


class DummyModel(models.Model):
    """
    Dummy model for testing below
    """
    def get_absolute_url(self):
        return '/'


class TestSharedContent(TestCase):

    def setUp(self):
        self.slug = 'admin'

    @unittest.skip("Makes multiple generous assumptions about project behaviour")
    def test_template_media(self):
        """
        Ensures base template has required media files.
        """
        response = self.client.get(reverse('home'))
        static_url = settings.STATIC_URL
        favicon_url = '<link rel="shortcut icon" href="{}img/favicon.png">'.format(static_url)
        touch_icon = '<link rel="apple-touch-icon" href="{}img/touch-icon.png">'.format(STATIC_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(favicon_url in response.content)
        self.assertTrue(touch_icon in response.content)

    @unittest.skip("Makes multiple generous assumptions about project behaviour")
    def test_shared_context_processor(self):
        """
        Test results of shared context processor are in template
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('site' in response.context)
        self.assertTrue('now' in response.context)
        self.assertTrue('year' in response.context)
        self.assertTrue('ga_code' in response.context)
        self.assertTrue('project_name' in response.context)
        self.assertTrue('current_path' in response.context)
        self.assertTrue('last_seen' in response.context)
        self.assertTrue('last_seen_fuzzy' in response.context)
        self.assertTrue('theme' in response.context)
        self.assertTrue('authenticated_request' in response.context)


class TemplateTagsTests(TestCase):
    def setUp(self):
        self.test_list = ['apples', 'oranges']

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
