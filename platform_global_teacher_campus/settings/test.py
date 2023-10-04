"""
These settings are here to use during tests, because django requires them.

In a real-world use case, apps in this project are installed into other
Django applications, so these settings will not be used.
"""

from os.path import abspath, dirname, join


def root(*args):
    """
    Get the absolute path of the given path relative to the project root.
    """
    return join(abspath(dirname(__file__)), *args)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'default.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'platform_global_teacher_campus',
    'organizations',
)

LOCALE_PATHS = [
    root('platform_global_teacher_campus', 'conf', 'locale'),
]

ROOT_URLCONF = 'platform_global_teacher_campus.urls'

SECRET_KEY = 'insecure-secret-key'

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': False,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',  # this is required for admin
            'django.contrib.messages.context_processors.messages',  # this is required for admin
        ],
    },
}]


CVW_COURSES_BACKEND = "platform_global_teacher_campus.edxapp_wrapper.backends.tests.courses_v1"
FORCE_PUBLISH_BACKEND = "platform_global_teacher_campus.edxapp_wrapper.backends.tests.force_publish_v1"
COURSE_ROLE_BACKEND = "platform_global_teacher_campus.edxapp_wrapper.backends.tests.course_roles_v1"
FORCE_PUBLISH_COMMAND_BACKEND = "platform_global_teacher_campus.edxapp_wrapper.backends.tests.force_publish_command_v1"
REQUEST_UTILS_BACKEND = "platform_global_teacher_campus.edxapp_wrapper.backends.tests.request_utils_v1"
