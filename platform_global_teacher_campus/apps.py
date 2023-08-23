"""
platform_global_teacher_campus Django application initialization.
"""

from django.apps import AppConfig


class PlatformGlobalTeacherCampusConfig(AppConfig):
    """
    Configuration for the platform_global_teacher_campus Django application.
    """

    name = 'platform_global_teacher_campus'
    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'plugin-cvw',
                'regex': r'^plugin-cvw/',
                'relative_path': 'urls',
            }
        },
        'settings_config': {
            'lms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
            },
        },
    }

class PlatformGlobalTeacherCampusCMSConfig(PlatformGlobalTeacherCampusConfig):
    """App configuration"""
    name = 'platform_global_teacher_campus'

    plugin_app = {
        'url_config': {
            'cms.djangoapp': {
                'namespace': 'plugin-cvw',
                'regex': r'^plugin-cvw/',
                'relative_path': 'urls',
            }
        },
        'settings_config': {
            'cms.djangoapp': {
                'common': {'relative_path': 'settings.common'}
            },
        },
    }