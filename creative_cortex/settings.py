from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config("SECRET_KEY", default='')

DEBUG = True

ALLOWED_HOSTS = []
#'creative-cortex.herokuapp.com'

INSTALLED_APPS = [
    'baton',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cc_app',

    'storages',
    'baton.autodiscover',

    'phonenumber_field',
    'admin_reorder'


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder'
]

ROOT_URLCONF = 'creative_cortex.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'creative_cortex.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config("DATABASE_NAME_2", default=''),
        'USER': config('DATABASE_USER_2', default=''),
        'HOST': config('DATABASE_HOST_2', default=''),
        'PORT': config('DATABASE_PORT_2', default='3306', cast=float),
        'PASSWORD': config('DATABASE_PASS_2', default=''),
        'OPTIONS': {'sql_mode': 'traditional'}}
}

#S3 Config

USE_S3 = config("USES3", default='False') == 'TRUE'
AWS_S3_ADDRESSING_STYLE = "virtual"

if USE_S3 == True:
    # aws settings
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default='')
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default='')
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default='')

    AWS_DEFAULT_ACL = None

    AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default='')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    #PUBLIC_MEDIA_LOCATION = 'media'
    #MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    #DEFAULT_FILE_STORAGE = 'creative_cortex.storage_backends.PublicMediaStorage'

    PRIVATE_MEDIA_LOCATION = 'private'
    PRIVATE_FILE_STORAGE = 'creative_cortex.storage_backends.PrivateMediaStorage'

else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



ADMIN_REORDER = (
    # Keep original label and models

    # Rename app
    #{'app': 'cc_app', 'label': 'creative-cortex-cms'},

    # Reorder app models
    {'app': 'cc_app', 'models': (
        'cc_app.Comics',
        'cc_app.Volumes',
        'cc_app.Chapters',
        'cc_app.Pages',
        'cc_app.Personnel',
        'cc_app.Comic_Personnel',
        'cc_app.Landing_Page_Images',
        'cc_app.Gallery_images',
        'cc_app.Web_Pages',
        'cc_app.Web_Page_Text_Content',
        'cc_app.Featured_Youtube_videos'
        'cc_app.Inquiries',


    )},

)


