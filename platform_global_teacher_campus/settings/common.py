"""
Settings for platform-global-teacher-campus
"""


def plugin_settings(settings):
    settings.CVW_COURSES_BACKEND = "platform_global_teacher_campus.edxapp_wrapper.backends.courses_v1"
    settings.FORCE_PUBLISH_BACKEND = "platform_global_teacher_campus.edxapp_wrapper.backends.force_publish_v1"
    settings.COURSE_ROLE_BACKEND = "platform_global_teacher_campus.edxapp_wrapper.backends.course_roles_v1"
    force_pub_command = "platform_global_teacher_campus.edxapp_wrapper.backends.force_publish_command_v1"
    settings.FORCE_PUBLISH_COMMAND_BACKEND = force_pub_command
    settings.REQUEST_UTILS_BACKEND = "platform_global_teacher_campus.edxapp_wrapper.backends.request_utils_v1"

    plugin_context_processor = 'platform_global_teacher_campus.context_processor.validation_panel_info'
    if plugin_context_processor not in settings.TEMPLATES[0]['OPTIONS']['context_processors']:
        settings.TEMPLATES[0]['OPTIONS']['context_processors'] += (plugin_context_processor,)
    if plugin_context_processor not in settings.TEMPLATES[1]['OPTIONS']['context_processors']:
        settings.TEMPLATES[1]['OPTIONS']['context_processors'] += (plugin_context_processor,)

    settings.DEFAULT_TEMPLATE_ENGINE = settings.TEMPLATES[0]
