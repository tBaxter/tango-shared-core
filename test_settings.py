from django.conf.global_settings import MIDDLEWARE

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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'tango_shared.context_processors.site_processor'
            ],
        },
    },
]