import os
from configurations import Configuration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Dev(Configuration):
    SECRET_KEY = '2k7!qwmji9krkju195d*%#5lbrvt)86@pb(uwr!n-f^k)b3dc&'

    DEBUG = True

    ALLOWED_HOSTS = []

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'restaurants',
        'menus',
        'users',
        'profiles',
        'api',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',
        'friendship',
        'coverage',
        'django_nose',
        'bootstrap4',
        'rest_framework',



    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'RestaurantPick.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['templates', 'templatetags',
                     ],
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

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
        'django.template.loaders.app_directories.load_template_source',
    )

    AUTHENTICATION_BACKENDS = (

        # Needed to login by username in Django admin, regardless of `allauth`
        'django.contrib.auth.backends.ModelBackend',

        # `allauth` specific authentication methods, such as login by e-mail
        'allauth.account.auth_backends.AuthenticationBackend',

    )

    WSGI_APPLICATION = 'RestaurantPick.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

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

    LANGUAGE_CODE = 'pl'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATICFILES_DIRS = [
        MEDIA_ROOT
    ]
    SITE_ID = 3

    AUTH_USER_MODEL = 'users.RestaurantUser'
    LOGIN_REDIRECT_URL = 'home'
    ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    SOCIALACCOUNT_PROVIDERS = {
        'facebook': {
            'METHOD': 'js_sdk',
            'SCOPE': ['email', 'public_profile'],
            'VERSION': 'v2.12',
        }
    }

    # REST_FRAMEWORK = {
    #
    #     'DEFAULT_PERMISSION_CLASSES': [
    #         'rest_framework.permissions.IsAuthenticated'
    #     ],
    #     'DEFAULT_AUTHENTICATION_CLASSES': [
    #         'rest_framework.authentication.SessionAuthentication',
    #         'rest_framework.authentication.BasicAuthentication'
    #     ]
    # }


    # TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    #
    # NOSE_ARGS = [
    #     '--with-coverage',
    #     '--cover-package=profiles, menus, users, restaurants, api/restaurants',
    #     '--cover-html',
    # ]


class Prod(Dev):
    ALLOWED_HOSTS = []
    DEBUG = False
    EMAIL_BACKEND = ''

