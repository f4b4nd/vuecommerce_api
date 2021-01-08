"""
Django settings for ecommerce project.
Generated by 'django-admin startproject' using Django 2.2.10.
"""

import os
from corsheaders.defaults import default_headers


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'accounts',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',

]

MIDDLEWARE = [

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.media',

            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database

DATABASES = {

    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': os.getenv('POSTGRES_NAME', ''),
        'USER': os.getenv('POSTGRES_USER', ''),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': os.getenv('POSTGRES_HOST', ''),
        'PORT': os.getenv('POSTGRES_PORT', ''),
    },

    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },

}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# KEY
SECRET_KEY = os.getenv('SECRET_KEY', '')

# Internationalization
LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# DEBUG 
DEBUG = os.getenv('DEBUG', False) == 'TRUE'
TEMPLATE_DEBUG = os.getenv('TEMPLATE_DEBUG', False) == 'TRUE'
DEBUG_PROPAGATE_EXCEPTIONS = os.getenv('DEBUG_PROPAGATE_EXCEPTIONS', False) == 'TRUE'

# HOSTS
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# CROSS ORIGINS WITH REST-FRAMEWORK
CORS_ALLOW_CREDENTIALS = os.getenv('CORS_ALLOW_CREDENTIALS', False) == 'TRUE'
CORS_ORIGIN_WHITELIST =  os.getenv('CORS_ORIGIN_WHITELIST', '').split(',')
CORS_ORIGIN_ALLOW_ALL = os.getenv('CORS_ORIGIN_ALLOW_ALL', False) == 'TRUE'
CORS_ALLOW_HEADERS = default_headers + (
    'Access-Control-Allow-Origin',
)

# Static files
STATIC_URL = '/static/'

# MEDIA 
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# MEDIA with S3 Configuration
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', None)
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', None)

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_REGION_NAME = 'eu-west-3'
AWS_S3_ADDRESSING_STYLE = "virtual"

# USER MODEL
AUTH_USER_MODEL = 'accounts.User'

# REST AUTHENTIFICATION
REST_FRAMERWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES' : [
        # which auth method (ex: token, session, etc.) is used when specific permission is required 
        'rest_framework.authentication.TokenAuthentication', 
    ],

    'DEFAULT_PERMISSION_CLASSES' : [
        # which level of permission (ex: authenticated, admin, etc.)
        'rest_framework.permissions.IsAuthenticated',
    ],
    
}

# STRIPE
STRIPE_TEST_PUBLIC_KEY = os.getenv('STRIPE_TEST_PUBLIC_KEY', None)
STRIPE_TEST_SECRET_KEY = os.getenv('STRIPE_TEST_SECRET_KEY', None)
STRIPE_LIVE_MODE = os.getenv('STRIPE_LIVE_MODE', False) == 'TRUE'
# DJSTRIPE_WEBHOOK_SECRET = os.getenv('DJSTRIPE_WEBHOOK_SECRET', 'whsec_xxx')