"""
NOTE: Repair the django-debug-toolbar, it is not showing.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_ROOT = os.path.join(BASE_DIR,'static')
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u_pax%c20ra1*nzf4j$h-4ij@)hz$_40-$3zvc!p2p7vvy!89-'

TWILIO_NUMBER = '+13018046980'
TWILIO_ACCOUNT_SID = 'ACc19ae2dada438cb0b5cf542946eaa2c2'
TWILIO_AUTH_TOKEN = '2abf088f138a5f496c854fff722c741e'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]
INTERNAL_IPS = ['*',]

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Jet settings
JET_DEFAULT_THEME = 'light-green'

JET_SIDE_MENU_ITEMS = [  # A list of application or custom item dicts
    {'label': 'AIP Main', 'app_label': 'aip_main', 'items': [
        {'name': 'aip_main.slider'},
        {'name': 'aip_main.shoutouts'},
    ]},
    {'label': 'AIP Workforce', 'app_label': 'workforce', 'items': [
        {'name': 'workforce.basicprofile'},
        {'name': 'workforce.employeeprofile'},
        {'name': 'workforce.accounts'},
        {'name': 'workforce.family'},
        {'name': 'workforce.workhistory'},
    ]},
    {'label': 'Users', 'items': [
        {'name': 'auth.user'},
        {'name': 'auth.group'},
        {'name': 'auth.userprofile', 'permissions': ['auth.user']},
    ]},
]

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',

    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',

    'django.contrib.humanize',

    'crispy_forms',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'mathfilters',

    'workforce',
    'fleet',
    'fuel',
    'operation',
    'warehouse',
    'accounting',
    'gallery',
    'tutorials',

    'django.contrib.sites',
    'markdown_deux',
    'bootstrapform',
    'import_export',

    'logentry_admin',
    'rangefilter',
    'django_filters',
    'widget_tweaks',

    'rest_framework',
    'taggit',

]

#Gallery Settings
GALLERY_LOGO_PATH = ""
GALLERY_TITLE = "Project Gallery"
GALLERY_FOOTER_INFO = "AIP Copyright 2019"
GALLERY_FOOTER_EMAIL = ""
GALLERY_THEME_COLOR = "black"


SITE_ID = 1

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'aip.login_required_middleware.LoginRequiredMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',

]

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.BasicAuthentication',
#         # 'rest_framework.authentication.SessionAuthentication',

#     ),
# }


ROOT_URLCONF = 'aip.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'aip.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eakdev$aip_db',
        'USER': 'eakdev',
        'PASSWORD': 'AIP_MySQL_Database',
        'HOST': 'eakdev.mysql.pythonanywhere-services.com',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LEAFLET_CONFIG = {
    'SPATIAL_EXTENT': (5.0, 44.0, 7.5, 46)
}

DEBUG_TOOLBAR_PATCH_SETTINGS = False


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_L10N = True

#USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'


#Setting for Sending Email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'aip911dispatch@gmail.com'
EMAIL_HOST_PASSWORD = 'mwzeyaijdcudmkwh'
EMAIL_PORT = 587



DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

