"""
The pipeline module defines custom Filters functions that are used in openedx-filters.
"""
from openedx_filters import PipelineStep
from platform_global_teacher_campus.edxapp_wrapper.force_publish import get_force_publish_course

ForcePublishCourseRenderStarted = get_force_publish_course()


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
            "org.openedx.studio.contentstore.modify_usage_key_ request.started.v1": {
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

        if request.json.get('publish') == 'make_public':
            request.json['publish'] = None

        course_key = str(course_key)


        return request
