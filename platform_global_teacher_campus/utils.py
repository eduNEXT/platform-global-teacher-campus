"""
All utils we can use across the plugin.
"""
from platform_global_teacher_campus.edxapp_wrapper.opaque_keys import get_usage_key
from platform_global_teacher_campus.edxapp_wrapper.request_utils import get_course_id_from_url

UsageKey = get_usage_key()
course_id_from_url = get_course_id_from_url()

def get_course_id_from_url(url):
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
    except UsageKey.InvalidKeyError:
        return None
