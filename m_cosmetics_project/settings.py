"""
Django settings for m_cosmetics_project project.
"""

import os
import dj_database_url
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',
    'store',
    'delivery',
    'orders',
    'payments',
    'inventory',
    'whatsapp_integration',
    'ai_assistant',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',          # ← serve static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'axes.middleware.AxesMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'm_cosmetics_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'm_cosmetics_project.wsgi.application'


# Database
# Uses DATABASE_URL env var on Render (PostgreSQL).
# Falls back to SQLite for local development.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Authentication backends (required by django-axes)
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Harare'
USE_I18N = True
USE_TZ = True


# Static files — WhiteNoise serves them in production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication Settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'product_list'

# Paynow Payment Gateway
PAYNOW_INTEGRATION_ID = config('PAYNOW_INTEGRATION_ID', default='')
PAYNOW_INTEGRATION_KEY = config('PAYNOW_INTEGRATION_KEY', default='')
PAYNOW_RESULT_URL = config('PAYNOW_RESULT_URL', default='http://localhost:8000/payment/callback/')
PAYNOW_RETURN_URL = config('PAYNOW_RETURN_URL', default='http://localhost:8000/payment/return/')

# AI Assistant (Claude API)
AI_API_KEY = config('AI_API_KEY', default='')
AI_MODEL = config('AI_MODEL', default='claude-opus-4-6')

# WhatsApp Business Cloud API
WA_ACCESS_TOKEN = config('WA_ACCESS_TOKEN', default='')
WA_PHONE_NUMBER_ID = config('WA_PHONE_NUMBER_ID', default='')
WA_VERIFY_TOKEN = config('WA_VERIFY_TOKEN', default='')

# Meta / Social Media
FB_PAGE_ACCESS_TOKEN = config('FB_PAGE_ACCESS_TOKEN', default='')
FB_PAGE_ID = config('FB_PAGE_ID', default='')
IG_ACCOUNT_ID = config('IG_ACCOUNT_ID', default='')

# django-axes: brute force protection
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']

# HTTPS / secure cookie settings (active when DEBUG=False)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # needed behind Render's proxy
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Contact information (edit via .env or Render env vars)
CONTACT_INFO = {
    'whatsapp': config('CONTACT_WHATSAPP', default=''),
    'cell': config('CONTACT_CELL', default=''),
    'email': config('CONTACT_EMAIL', default=''),
    'facebook': config('CONTACT_FACEBOOK', default=''),
    'tiktok': config('CONTACT_TIKTOK', default=''),
}
