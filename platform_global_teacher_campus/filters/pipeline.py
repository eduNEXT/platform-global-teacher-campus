"""
The pipeline module defines custom Filters functions that are used in openedx-filters.
"""
from openedx_filters import PipelineStep
from platform_global_teacher_campus.edxapp_wrapper.force_publish import get_force_publish_course
from platform_global_teacher_campus.edxapp_wrapper.courses import get_course_overview
from platform_global_teacher_campus.edxapp_wrapper.organizations import get_organization_model
from platform_global_teacher_campus.models import ValidationRules

ForcePublishCourseRenderStarted = get_force_publish_course()
CourseOverview = get_course_overview()
Organization = get_organization_model()


class StopForcePublishCourseRender(PipelineStep):
    """
    Stop account settings render process raising RedirectToPage exception.

    Example usage:

    Add the following configurations to your configuration file:

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.studio.manages.force_publish.render.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "platform_global_teacher_campus.filters.pipeline.StopForcePublishCourseRender"
                ]
            }
        },
    """
    def run_filter(self, context, *args, **kwargs):  # pylint: disable=arguments-differ
        """
        Pipeline step that stop force publish course page.
        """
        raise ForcePublishCourseRenderStarted.RedirectToPage(
            "You can't access to account settings.",
            redirect_to="",
        )


class ModifyRequestToBlockCourse(PipelineStep):
    """
    Stop account settings render process raising RedirectToPage exception.
    Example usage:
    Add the following configurations to your configuration file:
        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.studio.contentstore.modify_usage_key_request.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "platform_global_teacher_campus.filters.pipeline.ModifyRequestToBlockCourse"
                ]
            }
        },
    """
    def run_filter(self, request, course_key, *args, **kwargs):  # pylint: disable=arguments-differ
        """
        Pipeline step that stop publish course page.
        """
        course_key = str(course_key)
        course = CourseOverview.objects.get(course_id=course_key)

        if ValidationRules.objects.filter(is_active=True, organization__short_name=course.org).exists():
            return request

        # Disable publish button
        request.json['publish'] = None
        return request
