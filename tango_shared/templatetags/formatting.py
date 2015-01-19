from __future__ import print_function

import six

from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


@register.filter
def replace(value, arg):
    """
    Replaces one string with another in a given string
    usage: {{ foo|replace:"aaa|xxx"}}
    """

    replacement = arg.split('|')
    try:
        return value.replace(replacement[0], replacement[1])
    except:
        return value


@register.filter
def fixbreaks(value):
    """
    fixes line breaks to make markdown happy.
    Be careful. It won't play nice with para breaks.
    """
    return value.replace('\n', '  \n')



@register.filter
def humanized_join(value, add_links=False):
    """
    Given a list of strings, format them with commas and spaces,
    but with 'and' at the end.

    >>> humanized_join(['apples', 'oranges', 'pears'])
    "apples, oranges, and pears"

    In a template, if mylist = ['apples', 'oranges', 'pears']
    then {{ mylist|humanized_join }}
    will output "apples, oranges, and pears"

    Passing the add_links option will wrap each item in a link.
    Note this requires that anything being passed has get_absolute_url() defined.

    then {{ mylist|humanized_join:'add_links' }}
    will output "<a href="...">apples</a>, <a href="...">oranges</a>, and <a href="...">pears</a>"

    """
    if add_links:
        try:
            value = ['<a href="%s">%s</a>' % (item.get_absolute_url(), item) for item in value]
        except AttributeError:
            print("You did not pass objects with get_absolute_url() method.")
            return
    else:
        # make everything a string to avoid errors
        value = [six.u(item) for item in value]

    if len(value) == 1:
        return mark_safe(value[0])
    if len(value) == 2:
        return mark_safe("%s and %s" % (value[0], value[1]))

    # join all but the last element
    all_but_last = ", ".join(value[:-1])
    return mark_safe("%s, and %s" % (all_but_last, value[-1]))
