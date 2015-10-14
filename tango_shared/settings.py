import django.conf.global_settings as DEFAULT_SETTINGS

### Tango-unique settings

# Thumbnail aliases determines default image sizes for easy-thumbnails
# These assume a standard 60px column + 20px gutter.
# See the grid CSS for details.
THUMBNAIL_ALIASES = {
    '': {
        'one_col':      {'size': (60, 60),   'autocrop': True, 'crop': 'smart', 'upscale': True},

        'two_col':      {'size': (140, 140), 'autocrop': True},
        'two_col_crop': {'size': (140, 140), 'autocrop': True, 'crop': 'smart', 'upscale': True},
        'two_col_vert': {'size': (140, 420), 'autocrop': True, 'crop': 'smart', 'upscale': True},

        'three_col':      {'size': (220, 220), 'autocrop': True},
        'three_col_crop': {'size': (220, 220), 'autocrop': True, 'crop': 'smart', 'upscale': True},
        'three_col_vert': {'size': (220, 660), 'autocrop': True},

        'four_col':      {'size': (300, 300), 'autocrop': True},
        'four_col_crop': {'size': (300, 300), 'autocrop': True, 'crop': 'smart', 'upscale': True},
        'four_col_vert': {'size': (300, 900), 'autocrop': True},

        'five_col':      {'size': (380, 380), 'autocrop': True},
        'five_col_crop': {'size': (380, 380), 'autocrop': True, 'crop': 'smart', 'upscale': True},
        'five_col_vert': {'size': (380, 900), 'autocrop': True},

        'six_col':      {'size': (460, 460), 'autocrop': True},
        'six_col_crop': {'size': (460, 460), 'autocrop': True, 'crop': 'smart', 'upscale': True},
        'six_col_vert': {'size': (460, 900), 'autocrop': True},

        'seven_col':      {'size': (540, 540), 'autocrop': True},
        'seven_col_crop': {'size': (540, 540), 'autocrop': True, 'crop': 'smart', 'upscale': True},
        'seven_col_vert': {'size': (540, 1080), 'autocrop': True},

        'eight_col':      {'size': (620, 620), 'autocrop': True},
        'eight_col_crop': {'size': (620, 620), 'autocrop': True, 'crop': 'smart', 'upscale': True},
        'eight_col_vert': {'size': (620, 1240), 'autocrop': True},

        'nine_col':      {'size': (700, 700), 'autocrop': True},
        'nine_col_crop': {'size': (700, 700), 'autocrop': True, 'crop': 'smart', 'upscale': True},
        'nine_col_vert': {'size': (700, 1400), 'autocrop': True},

        'ten_col':      {'size': (780, 780), 'autocrop': True},
        'ten_col_crop': {'size': (780, 780), 'autocrop': True, 'crop': 'smart', 'upscale': True},
        'ten_col_vert': {'size': (780, 1560), 'autocrop': True},

        'eleven_col':      {'size': (860, 860), 'autocrop': True},
        'eleven_col_crop': {'size': (860, 860), 'autocrop': True, 'crop': 'smart', 'upscale': True},
        'eleven_col_vert': {'size': (860, 1640), 'autocrop': True},

        'twelve_col':      {'size': (940, 940), 'autocrop': True},
        'twelve_col_crop': {'size': (940, 940), 'autocrop': True, 'crop': 'smart', 'upscale': True},
        'twelve_col_vert': {'size': (940, 1880), 'autocrop': True},
    },
}

# sets default pagination
PAGINATE_BY = 25

# Google analytics GA code
GOOGLE_ANALYTICS_ID = ''

# Project name
PROJECT_NAME = 'tango'

# if set to false, RESTRICT_CONTENT_TO_SITE will allow
# sites/projects to share content.
# If true, content will be limited to the current site.
RESTRICT_CONTENT_TO_SITE = True

# If your site is a news source, set to True.
# This will attach the name of your organization to articles
# as well as add extra fields news organizations need,
# including options to mark content as
# opinion/editorial, dateline, and noting another source as
# the origin of the content.
NEWS_SOURCE = True

# Comment moderation settings
# Number of days after publication until comments close:
COMMENTS_CLOSE_AFTER = 30
# Number of days after publication until comments require moderation:
COMMENTS_MOD_AFTER = 15


# tango apps will be added to installed apps. Or should be.
TANGO_APPS = (
    'tango_capo',
    'tango_shared',
    'user_profiles',
    'articles',
    'autotagger',
    'contact_manager',
    'happenings',
    'photos',
    'video',
    'typogrify',
    'voting',
    'easy_thumbnails',
)


### Django settings...

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Adds Context processors you'll want.
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'tango_shared.context_processors.site_processor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
