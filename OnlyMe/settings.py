"""
Django settings for OnlyMe project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6(a81!x@v)nzopwl8qmxw$z@+(mdp+0e32cg75&p_ob*9&f%e_'

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('ENV') == 'PRODUCTION':
    DEBUG = True
else:
    DEBUG = True

ALLOWED_HOSTS = [
        'lechatonguniverse.herokuapp.com',
        '127.0.0.1',
        '172.16.145.118'
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'MoviesAndMe.apps.MoviesandmeConfig',
    'LeChApi.apps.LechapiConfig',
]
#'django_telegrambot',
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

#REST_FRAMEWORK = {
#    'DEFAULT_PERMISSION_CLASSES' : [
#        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#    ]
#}

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'OnlyMe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.i18n",
            ],
        },
    },
]

WSGI_APPLICATION = 'OnlyMe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lechatonguniverse',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '',
        'PORT': '5432',
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

TELEGRAM_API_ID = 1315849

TELEGRAM_HASH_ID = 'e61ce3f911e5123e2cd8ec2b4e713935'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext = lambda x: x

from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
   ('fr', _('French')),
   ('en', _('English')),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_URL = '/media/'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, '/locale/'),
)

#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)

API_KEY_MOVIE = 'f972c58efb26ab0a5e82cda1f7352586'

if os.environ.get('ENV') == 'PRODUCTION':
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
    STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, 'static'),
    )
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)


DJANGO_TELEGRAMBOT = {

    'MODE' : 'WEBHOOK', #(Optional [str]) # The default value is WEBHOOK,
                        # otherwise you may use 'POLLING'
                        # NB: if use polling you must provide to run
                        # a management command that starts a worker

    'WEBHOOK_SITE' : 'https://c6c37f80.ngrok.io',
    'WEBHOOK_PREFIX' : 'https://c6c37f80.ngrok.io', # (Optional[str]) # If this value is specified,
                                  # a prefix is added to webhook url

    #'WEBHOOK_CERTIFICATE' : 'cert.pem', # If your site use self-signed
                         #certificate, must be set with location of your public key
                         #certificate.(More info at https://core.telegram.org/bots/self-signed )

    'BOTS' : [
        {
           'TOKEN': '914995992:AAFPpnVKjnG6lFcmF5FUctkjN7HtKVQrugA', #Your bot token.

           'ALLOWED_UPDATES':['*',] #(Optional[list[str]]), # List the types of
                                                   #updates you want your bot to receive. For example, specify
                                                   #``["message", "edited_channel_post", "callback_query"]`` to
                                                   #only receive updates of these types. See ``telegram.Update``
                                                   #for a complete list of available update types.
                                                   #Specify an empty list to receive all updates regardless of type
                                                   #(default). If not specified, the previous setting will be used.
                                                   #Please note that this parameter doesn't affect updates created
                                                   #before the call to the setWebhook, so unwanted updates may be
                                                   #received for a short period of time.

           #'TIMEOUT':(Optional[int|float]), # If this value is specified,
                                   #use it as the read timeout from the server

           #'WEBHOOK_MAX_CONNECTIONS':(Optional[int]), # Maximum allowed number of
                                   #simultaneous HTTPS connections to the webhook for update
                                   #delivery, 1-100. Defaults to 40. Use lower values to limit the
                                   #load on your bot's server, and higher values to increase your
                                   #bot's throughput.

           #'POLL_INTERVAL' : (Optional[float]), # Time to wait between polling updates from Telegram in
                           #seconds. Default is 0.0

           #'POLL_CLEAN':(Optional[bool]), # Whether to clean any pending updates on Telegram servers before
                                   #actually starting to poll. Default is False.

           #'POLL_BOOTSTRAP_RETRIES':(Optional[int]), # Whether the bootstrapping phase of the `Updater`
                                   #will retry on failures on the Telegram server.
                                   #|   < 0 - retry indefinitely
                                   #|     0 - no retries (default)
                                   #|   > 0 - retry up to X times

           #'POLL_READ_LATENCY':(Optional[float|int]), # Grace time in seconds for receiving the reply from
                                   #server. Will be added to the `timeout` value and used as the read timeout from
                           #server (Default: 2).
        },
        #Other bots here with same structure.
    ],

}