"""
Django settings for Commissions project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%0951uw)u5*v84azua8hkddlg($#af)@-aab-4!egevy_8vnz%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_markdown',
    'bootstrap3',
    'Coms',
    'Auth',
    'UserControl',
    'sorl.thumbnail',
    'hooks',
    'tz_detect',
    'rest_framework',
    'Characters',
    'Navigation'

)

STATICFILES_DIRS = ('Commissions/static',)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['Commissions/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tz_detect.middleware.TimezoneMiddleware',
)

ROOT_URLCONF = 'Commissions.urls'

WSGI_APPLICATION = 'Commissions.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        "HOST": '127.0.0.1',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'NAME': 'commissions'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static/'

MARKDOWN_EDITOR_SKIN = 'simple'
MARKDOWN_SET_PATH = "Coms/"

AUTH_PROFILE_MODULE = 'UserControl.UserProfile'

LOGIN_URL = '/account/login'
LOGIN_REDIRECT_URL = '/user/'

MEDIA_ROOT = BASE_DIR + '/media/'
MEDIA_URL = '/media/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
    }
}

BOOTSTRAP3 = {
    'set_required': False
}
MARKDOWN_EXTENSIONS = ['ComMarkup:ComsMarkdown']
TZ_DETECT_COUNTRIES = ('US', 'CA', 'EU', 'GB')

THUMBNAIL_DEBUG = True
