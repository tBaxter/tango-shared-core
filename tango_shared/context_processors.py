import datetime

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

now = datetime.datetime.now()
one_day_ago = now - datetime.timedelta(days=1)

def site_processor(request):
    
    ALLOWABLE_THEMES = getattr(settings, 'ALLOWABLE_THEMES', None)
    authenticated_request = request.user.is_authenticated

    # Resolve theme by cookie, user attr, or default, in that order
    theme = request.COOKIES.get('theme', None)
    if not theme:
        theme = getattr(request.user, "theme", None)
    if not theme or theme not in ALLOWABLE_THEMES:
        theme = getattr(settings, 'DEFAULT_THEME', None)

    last_seen = request.session.get('last_seen', now)
    last_seen_fuzzy = last_seen
    if last_seen > one_day_ago:
        last_seen_fuzzy = one_day_ago

    return {
        'site': get_current_site(request),
        'now': now,
        'project_name': getattr(settings, 'PROJECT_NAME', None),
        'current_path': request.get_full_path(),
        'last_seen': last_seen,
        'last_seen_fuzzy': last_seen_fuzzy,
        'theme': theme,
        'authenticated_request': authenticated_request,
    }
