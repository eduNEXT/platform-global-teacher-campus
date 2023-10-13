"""
The pipeline module defines custom Filters functions that are used in openedx-filters.
"""

import logging

from openedx_filters import PipelineStep
from organizations.models import Organization

from platform_global_teacher_campus.edxapp_wrapper.courses import get_course_overview
from platform_global_teacher_campus.edxapp_wrapper.force_publish import get_force_publish_course
from platform_global_teacher_campus.models import ValidationProcess, ValidationProcessEvent, ValidationRules
from platform_global_teacher_campus.unable_publish_or_update import UnablePublishOrUpdate

log = logging.getLogger(__name__)

ForcePublishCourseRenderStarted = get_force_publish_course()
CourseOverview = get_course_overview()


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

    def run_filter(     # pylint: disable=arguments-differ, inconsistent-return-statements
            self,
            request,
            course_key,
            *args,
            **kwargs):
        """
        Pipeline step that stop publish course page.
        """
        course_key = str(course_key)
        course = CourseOverview.objects.get(id=course_key)

        organization = Organization.objects.get(short_name=course.org)

        is_org_excluded = ValidationRules.objects.filter(
            permission_type=ValidationRules.PermissionTypeChoices.ORG_EXCLUDED,
            organization=organization,
            is_active=True,
        ).exists()

        if is_org_excluded:
            log.info("Permission type is ORG_EXCLUDED for %s. Publishing course %s.", course.org, course)
            return request

        if "data" in request.json:
            if not ValidationProcess.objects.filter(course=course).exists():
                log.info("Can create a new course without validation process")
                return request

            is_status_draft = ValidationProcessEvent.objects.filter(
                validation_process=ValidationProcess.objects.get(course=course),
                status=ValidationProcessEvent.StatusChoices.DRAFT,
            ).exists()

            if not is_status_draft:
                raise UnablePublishOrUpdate("Can not edit a couse. status is not draft.")

        # Disable publish button
        if "publish" in request.json and request.json["publish"] == "make_public":
            raise UnablePublishOrUpdate("Can not edit a couse. status is not draft.")
