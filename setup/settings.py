import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@jdf01zf3u9vyqv62^kjf=f2%^#sh2taf0x=6%#o0-_xa=1gb*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Email Settings
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

BOOTSTRAP3 = {
    'javascript_in_head': True,
}
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',

    'djmoney',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    # INSTALLED APPS
    'pams_system',
    'django_bootstrap3_multidatepicker',
    'bootstrap_modal_forms',
    'bootstrap3',
    'mptt',
    'crispy_forms',
    'phonenumber_field',
    'rest_framework',
    'widget_tweaks',
    'webpush',
    'mathfilters',
    'django_extensions',
    'django_select2',
    'django_filters',
    'notifications',

    # PROJECT APPS
    'dashboard',
    'accounts',
    'employee',
    'leave',
    'taskmanager',
    'reports',
    'crm'
]

ASGI_APPLICATION = "setup.asgi.application"


SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setup.urls'
# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend',
# )

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'taskmanager.context_processors.get_teams',
                'taskmanager.context_processors.get_task_analysis',
                'taskmanager.context_processors.get_subtask_analysis',
                'taskmanager.context_processors.get_notifications',
                'leave.context_processors.get_leaves',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = { 
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': os.getenv('DB_NAME', 'performance'),
		'PASSWORD': os.getenv('DB_PASSWORD', 'luther1996-'),
		'HOST': os.getenv('DB_HOST', 'localhost'),
		'USER': os.getenv('DB_USER', 'postgres'),
		'PORT': os.getenv('DB_PORT', 5432),
	 }

	 
    
}


PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": "[your api key]",
    "GCM_API_KEY": "[your api key]",
    "APNS_CERTIFICATE": "/path/to/your/certificate.pem",
    "APNS_TOPIC": "com.example.push_test",
    "WNS_PACKAGE_SECURITY_ID": "[your package security id, e.g: 'ms-app://e-3-4-6234...']",
    "WNS_SECRET_KEY": "[your app secret key, e.g.: 'KDiejnLKDUWodsjmewuSZkk']",
    "WP_PRIVATE_KEY": "/path/to/your/private.pem",
    "WP_CLAIMS": {'sub': "mailto: development@example.com"}
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

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BE-PoVEuQGI-OUPkpphW1ivIj2A6SskYXRn9v7cJk6bMDr8BAXVIqqg478x3OMh8ON-tkp-vlHW7-y3NwxYle9o",
    "VAPID_PRIVATE_KEY": "qnfCLlhFxXoFlVjmTbQAeMs7zZrNGXZxd9GLSH8vqJc",
    "VAPID_ADMIN_EMAIL": "tutorialcreation81@gmail.com"
}
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# STATIC FILES WILL BE SERVED FROM STATIC_CDN WHEN WE ARE LIVE - OUT SIDE OF PROJECT
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# THIS KEEPS THE PROJECT FILES - CSS/JS/IMAGES/FONTS

# MEDIA - UPLOADED FILES/IMAGES
MEDIA_URL = '/media/'

# MEDIA FILES WILL BE SERVED FROM STATIC_CDN WHEN WE ARE LIVE
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn', 'media_root')


CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', '')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', '')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'hesbon.maiyo@actserv.co.ke')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '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')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD','Hesbon5600')
FROM_EMAIL ="brooks-no-reply@actserv.co.ke"
DEFAULT_FROM_EMAIL="brooks-no-reply@actserv.co.ke"
EMAIL_USE_TLS = True
EMAIL_SENDER = 'hesbon.dev@gmail.com'
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'


ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400 
ACCOUNT_LOGOUT_REDIRECT_URL ='/'
LOGIN_REDIRECT_URL = '/accounts/email/'
ACCOUNT_ADAPTER='performance.adapter.RestrictEmailAdapter'
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.12',
    },
     'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

TWILIO_ACCOUNT_SID='ACf12a703b1e1be2ed9f271e7a18bc8f87'
TWILIO_AUTH_TOKEN='58a4638655f0210c42f128caa8d4b57b'
TWILIO_NUMBER='+17609708434'
