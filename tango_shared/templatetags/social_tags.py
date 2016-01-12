from django import template
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.inclusion_tag('includes/social_links.html', takes_context=True)
def social_links(context, object, user=None, authed=False, downable=False, vote_down_msg=None):
    """
    Outputs social links. At minimum, this will be Facebook and Twitter.
    But if possible, it will also output voting and watchlist links.

    Usage:
    {% social_links object %}
    {% social_links object user %}
    {% social_links object user authenticated_request %}
    """
    # check if voting available
    voting = False
    if hasattr(object, 'votes'):
        voting = True

    return {
        'object': object,
        'url':    object.get_absolute_url(),
        'site':   get_current_site(context['request']),
        'ctype':  ContentType.objects.get_for_model(object),
        'user':   user,
        'voting': voting,
        'vote_down': downable,
        'vote_down_msg': vote_down_msg,
        'authenticated_request': authed,
    }
