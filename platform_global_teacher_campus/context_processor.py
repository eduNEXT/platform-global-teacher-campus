"""
This context processor is added to every request to render a mako or django template.
"""
from platform_global_teacher_campus.models import ValidationStatusMessage
from platform_global_teacher_campus.utils import (
    get_course_id_from_url,
    get_course_id_from_block,
)



def validation_status_message(request):
    """
    It inserts info from validation_status_message to every request to render a mako or django template.
    """
    try:
        course_id = get_course_id_from_url(request.headers['Host']+request.path)
        if not course_id:
            course_id = get_course_id_from_block(request.path.replace("/container/", ""))
        validation_status_message = ValidationStatusMessage.get_the_status_message_by_course_id(course_id=course_id)

    except:
        validation_status_message = None

    return validation_status_message if validation_status_message else {}
