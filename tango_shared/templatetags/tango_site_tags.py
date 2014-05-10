import datetime
from itertools import chain

from django import template
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.timesince import timesince
from django.utils.safestring import mark_safe


register = template.Library()


@register.inclusion_tag('includes/formatted_time.html')
def format_time(date_obj, time_obj=None, datebox=False, dt_type=None, classes=None):
    """
    Returns formatted HTML5 elements based on given datetime object.
    By default returns a time element, but will return a .datebox if requested.

    dt_type allows passing dt_start or dt_end for hcal formatting.
    link allows passing a url to the datebox.

    classes allows sending arbitrary classnames. Useful for properly microformatting elements.

    Usage:
    {% format_time obj.pub_date %}
    {% format_time obj.start_date 'datebox' 'dtstart' %}
    {% format_time obj.end_date obj.end_time 'datebox' 'dt_end' %}
    """
    if not time_obj:
        time_obj = getattr(date_obj, 'time', None)

    if dt_type:
        classes = '{0} {1}'.format(classes, dt_type)
    if datebox:
        classes = '{0} {1}'.format(classes, datebox)
    return {
        'date_obj': date_obj,
        'time_obj': time_obj,
        'datebox': datebox,
        'current_year': datetime.date.today().year,
        'classes': classes
    }


@register.filter
def short_timesince(date):
    """
    A shorter version of Django's built-in timesince filter.
    Selects only the first part of the returned string,
    splitting on the comma.

    Falls back on default Django timesince if it fails.

    Example: 3 days, 20 hours becomes "3 days".

    """
    try:
        return timesince(date).split(", ")[0]
    except IndexError:
        timesince(date)


@register.filter
def fix_indents(value):
    """
    Strips tabs and extra spaces from user-submitted text
    to avoid triggering pre code in markdown.

    Use this with caution.
    It's much better to sanitize the content before save().

    Likely to be replaced by a smarter minification.
    """
    value = value.replace('\t', '').replace('    ', ' ')
    return value


@register.inclusion_tag('includes/fresh_content.html')
def get_fresh_content(top=4, additional=10, featured=False):
    """
    Requires articles, photos and video packages to be installed.
    Returns published *Featured* content (articles, galleries, video, etc)
    and an additional batch of fresh regular (featured or not) content.
    The number of objects returned is defined when the tag is called.
    The top item type is defined in the sites admin for sites that
    have the supersites app enabled.
    If "featured" is True, will limit to only featured content.
    Usage:
        {% get_fresh_content 5 10 %}
        Would return five top objects and 10 additional
        {% get_fresh_content 4 8 featured %}
        Would return four top objects and 8 additional, limited to featured content.
    What you get:
        'top_item':       the top featured item
        'top_item_type':  the content type for the top item (article, gallery, video)
        'featured':       Additional featured items. If you asked for 5 featureed items, there will be 4
                          (five - the one that's in top item)
        'articles':       featured articles, minus the top item
        'galleries':      featured galleries, minus the top item
        'vids':           featured video, minus the top item,
        'more_articles':  A stack of articles, excluding what's in featured, sliced to the number passed for <num_regular>,
        'more_galleries': A stack of galleries, excluding what's in featured, sliced to the number passed for <num_regular>,
        'additional':     A mixed list of articles and galleries, excluding what's in featured, sliced to the number passed for <num_regular>,
    """
    from articles.models import Article
    from photos.models import Gallery
    from video.models import Video
    
    articles = Article.published.only('title', 'summary', 'slug', 'created')
    galleries = Gallery.published.only('title', 'summary', 'slug', 'created')
    videos = Video.published.only('title', 'summary', 'slug', 'created')

    if featured:
        articles = articles.filter(featured=True)
        galleries = galleries.filter(featured=True)
        videos = videos.filter(featured=True)

    # now slice to maximum possible for each group
    # and go ahead and make them lists for chaining
    max_total = top + additional
    articles = list(articles[:max_total])
    galleries = list(galleries[:max_total])
    videos = list(videos[:max_total])

    # chain the lists now
    content = chain(articles, galleries, videos)
    content = sorted(content, key=lambda instance: instance.created)
    content.reverse()

    top_content = content[:top]
    additional_content = content[top:max_total]
    return {
        'top_content': top_content,
        'additional_content': additional_content,
        'MEDIA_URL': settings.MEDIA_URL,
    }


@register.filter(is_safe=True)
def markdown(value, arg=''):
    """
    Runs Markdown over a given value, optionally using various
    extensions python-markdown supports.

    Derived from django.contrib.markdown, which was deprecated from django.

    ALWAYS CLEAN INPUT BEFORE TRUSTING IT.

    Syntax::

        {{ value|markdown:"extension1_name,extension2_name..." }}

    To enable safe mode, which strips raw HTML and only returns HTML
    generated by actual Markdown syntax, pass "safe" as the first
    extension in the list.

    If the version of Markdown in use does not support extensions,
    they will be silently ignored.

    """
    import warnings
    warnings.warn('The markdown filter has been deprecated',
                  category=DeprecationWarning)
    try:
        import markdown
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in 'markdown' filter: The Python markdown library isn't installed.")
        return force_text(value)
    else:
        markdown_vers = getattr(markdown, "version_info", 0)
        if markdown_vers < (2, 1):
            if settings.DEBUG:
                raise template.TemplateSyntaxError(
                    "Error in 'markdown' filter: Django does not support versions of the Python markdown library < 2.1.")
            return force_text(value)
        else:
            extensions = [e for e in arg.split(",") if e]
            if extensions and extensions[0] == "safe":
                extensions = extensions[1:]
                return mark_safe(markdown.markdown(
                    force_text(value), extensions, safe_mode=True, enable_attributes=False))
            else:
                return mark_safe(markdown.markdown(
                    force_text(value), extensions, safe_mode=False))

