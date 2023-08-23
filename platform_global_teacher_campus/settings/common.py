"""
Settings for platform-global-teacher-campus
"""

def plugin_settings(settings):
    settings.CVW_COURSES_BACKEND = "platform_global_teacher_campus.edxapp_wrapper.backends.courses_v1"
    settings.USER_MODEL_BACKEND = "platform_global_teacher_campus.edxapp_wrapper.backends.users_v1"
    settings.ORGANIZATIONS_BACKEND = "platform_global_teacher_campus.edxapp_wrapper.backends.organizations_v1"
