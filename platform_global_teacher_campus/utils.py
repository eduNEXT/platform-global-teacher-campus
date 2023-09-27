"""
All utils we can use across the plugin.
"""
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import UsageKey

from platform_global_teacher_campus.edxapp_wrapper.request_utils import get_course_id_from_url

course_id_from_url = get_course_id_from_url()


def get_course_id_from_url(url):    # pylint: disable=function-redefined
    """
    Gets course key from a url.
    """
    return course_id_from_url(url)


def get_course_id_from_block(block):
    """
    Gets course key from a block. e.g.
    'block-v1:edX+test+2023+type@vertical+block@0df8158f88374b03b12c45181726e64e'.
    """
    try:
        usage_key = UsageKey.from_string(block)
        return usage_key.course_key
    except InvalidKeyError:
        return None
