"""
Utils for publish a course.
"""
from opaque_keys.edx.keys import CourseKey

from platform_global_teacher_campus.edxapp_wrapper.force_publish_command import (
    get_course_versions_branches,
    get_force_publish_course_command,
    get_mixed_module_store,
    get_modulestore,
)

DraftVersioningModuleStore = get_force_publish_course_command()
modulestore = get_modulestore()
MixedModuleStore = get_mixed_module_store()
course_versions_branches = get_course_versions_branches()


def publish_course(course_id, user):
    course_key = CourseKey.from_string(str(course_id))
    versions = course_versions_branches(str(course_id))
    owning_store = modulestore()._get_modulestore_for_courselike(course_key)    # pylint: disable=protected-access

    updated_versions = owning_store.force_publish_course(
        course_key, user, 'commit'
    )
    if updated_versions:
        # if publish and draft were different
        if versions['published-branch'] != versions['draft-branch']:
            return f"Success! Published the course '{course_key}'.\nUpdated course versions : {updated_versions}"
        else:
            return f"Course '{course_key}' is already in published state."
    else:
        return f"Error! Could not publish course {course_key}."
