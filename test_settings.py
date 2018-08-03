import django.conf.global_settings import MIDDLEWARE, TEMPLATE_CONTEXT_PROCESSORS

SECRET_KEY = "lorem ipsum"

INSTALLED_APPS = (
    'easy_thumbnails',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'tango_shared',
    'voting',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
ROOT_URLCONF = 'test_urls'
SITE_ID = 1

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'tango_shared.context_processors.site_processor',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]