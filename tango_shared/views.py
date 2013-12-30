import os

import markdown
from django.conf import settings
from django.shortcuts import render
from django.utils.importlib import import_module
from django.views.generic import ListView, TemplateView, DetailView


class ContextListView(ListView):
    """ Allows passing extra_context through list view. """
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ContextListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class ContextTemplateView(TemplateView):
    """ Allows passing extra_context through template view. """
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ContextTemplateView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class ContextDetailView(DetailView):
    """ Allows passing extra_context through detail view. """
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ContextDetailView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


def build_howto(request=None):
    """
    Searches for "how_to.md" files in app directories.
    Creates user-friendly admin how-to section from apps that have them.
    """
    how_tos = {}

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        app_dir = os.path.dirname(mod.__file__)
        how_to_file = os.path.join(app_dir, 'how_to.md')

        if os.path.exists(how_to_file):
            contents = open(how_to_file).read()
            how_tos[app] = markdown.markdown(contents)
        
    return render(request, 'admin/how-to/index.html', {'how_tos': how_tos})
