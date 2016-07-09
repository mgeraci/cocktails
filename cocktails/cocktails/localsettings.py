DEBUG = True
STATIC_ROOT = 'staticfiles'
MEDIA_ROOT = 'mediafiles'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cocktails',
        'USER': 'dev',
        'PASSWORD': 'wdt6Rw6L$+66VqrTwsLwey%^K}8Tpq'
    }
}
