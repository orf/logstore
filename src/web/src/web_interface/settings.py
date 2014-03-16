"""
Django settings for web_interface project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.append(os.path.join(BASE_DIR, ".."))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w9)8ys*h4xzn%7g#@di#l3y%t))pn+9fw&rc$b@*e1v)g@2r*('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static_files"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'apps.dashboard',
    'apps.servers',
    'apps.search',
    'apps.formats',
    'apps.events',
    'apps.api',
    'apps.analyser',
    'apps.statistics',
    'apps.alerts',

    'logstore.ext.geoip_transformer',
    'logstore.ext.user_agent_transformer',
    'logstore.ext.http_request_transformer',

    'kronos',
    'djangojs',
    'django.contrib.admin',
    'debug_toolbar',
    'template_timings_panel',
    'crispy_forms',
    'crispy_forms_foundation',
    'django_activeurl',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    'utils.layout_context.layout_context'
)

INTERNAL_IPS = ('127.0.0.1', '192.168.137.1')
INTERCEPT_REDIRECTS = True

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

ROOT_URLCONF = 'web_interface.urls'

WSGI_APPLICATION = 'web_interface.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'logstore',
        'USER': 'logstore',
        'PASSWORD': 'password'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

CRISPY_TEMPLATE_PACK = 'foundation'

ACTIVE_URL_CACHE = False

CONDUCTOR_PORT = 6061

ELASTICSEARCH_URL = "http://localhost:9200/"

JS_URLS_NAMESPACES = ["api", "servers"]

PUSHBULLET_API_KEY = "581IHLazsXFe12egUsNgd0BDewNVh72A"

GEOIP_DATABASE_DIR = os.path.join(BASE_DIR, ".cache")
