import requests
import hashlib
import hmac
import json
import logging

from opaque_keys.edx.keys import CourseKey
from django.conf import settings
from platform_global_teacher_campus.edxapp_wrapper.force_publish_command import (
    get_course_versions_branches,
    get_force_publish_course_command,
    get_mixed_module_store,
    get_modulestore,
)

logger = logging.getLogger(__name__)


class CreateRichieCourseError(Exception):
    """Error trying to create a new Course in Richie."""
    pass


class SyncRichieCourseError(Exception):
    """Error trying to sync a course with Richie"""
    pass


class Richie:
    @staticmethod
    def get_sync_data(course_key) -> dict:
        course = get_modulestore().get_course(course_key)
        enrollment_start = course.enrollment_start and course.enrollment_start.isoformat()
        enrollment_end = course.enrollment_end and course.enrollment_end.isoformat()
        return {
            "resource_link": f"{settings.LMS_ROOT_URL}/courses/{course.id}/course",
            "start": course.start and course.start.isoformat(),
            "end": course.end and course.end.isoformat(),
            "enrollment_start": enrollment_start,
            "enrollment_end": enrollment_end,
            "languages": [course.language or settings.LANGUAGE_CODE],
        }

    @staticmethod
    def get_authorization_header(data):
        signature = hmac.new(
            settings.RICHIE_COURSE_HOOK["secret"].encode("utf-8"),
            msg=json.dumps(data).encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        return f"SIG-HMAC-SHA256 {signature}"

    def create_course(self, course_key) -> None:
        course = get_modulestore().get_course(course_key)
        data = {
            "organization_code": course.org,
            "course_code": course.display_number_with_default,
            "course_title": course.display_name,
        }

        response = requests.post(
            settings.RICHIE_COURSE_HOOK["create_endpoint"],
            json=data,
            headers={"Authorization": self.get_authorization_header(data=data)},
            timeout=30,
        )

        if response.status_code == 200:
            logger.info(f"Successfully created course {course.id} in Richie")

        if response.status_code >= 400:
            raise CreateRichieCourseError(
                f"Could not create course {course.id} in Richie. Response: {response.content.decode()}"
            )

    def sync_course(self, course_key):
        course = get_modulestore().get_course(course_key)
        data = self.get_sync_data(course_key)
        try:
            response = requests.post(
                settings.RICHIE_COURSE_HOOK["sync_endpoint"],
                json=data,
                headers={"Authorization": self.get_authorization_header(data=data)},
                timeout=settings.RICHIE_COURSE_HOOK["timeout"],
            )

            if response.status_code >= 400:
                raise SyncRichieCourseError(f"Could not synchronize course {course.id} with Richie. Response: {response.content.decode()}")
            else:
                logger.info(f"Successfully synchronized course {course.id} with Richie")
        except requests.exceptions.Timeout:
            raise SyncRichieCourseError(f"Could not synchronize course {course.id} with Richie. Response timeout")


def publish_course(course_id, user):
    course_key = CourseKey.from_string(str(course_id))
    versions = get_course_versions_branches(str(course_id))
    owning_store = get_modulestore()._get_modulestore_for_courselike(course_key)    # pylint: disable=protected-access

    # Create course in Richie
    richie = Richie()
    try:
        richie.create_course(course_key=course_key)
    except CreateRichieCourseError:
        return f"Error! Could not create course {course_key} in Richie."

    updated_versions = owning_store.force_publish_course(course_key, user, 'commit')
    if updated_versions:
        # Sync course in Richie
        try:
            richie.sync_course(course_key=course_key)
        except SyncRichieCourseError:
            return f"Error! Could not syncronize course {course_key} with Richie."

        # if publish and draft were different
        if versions['published-branch'] != versions['draft-branch']:
            return f"Success! Published the course '{course_key}'.\nUpdated course versions: {updated_versions}"
        else:
            return f"Course '{course_key}' is already in the published state."
    else:
        return f"Error! Could not publish course {course_key}."
