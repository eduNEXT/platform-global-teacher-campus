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
        
    }
