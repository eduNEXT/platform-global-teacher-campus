"""
This context processor is added to every request to render a mako or django template.
"""
from platform_global_teacher_campus.models import ValidationStatusMessage
from platform_global_teacher_campus.utils import get_course_id_from_block, get_course_id_from_url


def validation_panel_info(request):
    """
    It inserts info from validation_status_message to every request to render a mako or django template.
    """
    try:
        course_id = get_course_id_from_url(request.headers['Host'] + request.path)
        if not course_id:
            course_id = get_course_id_from_block(request.path.replace("/container/", ""))
        validation_status_message = ValidationStatusMessage.get_the_status_message_by_course_id(course_id=course_id)
        # Add the prefix validation_panel_ to be more clear in the frontend templates.
        panel_info = dict(
            map(lambda item: ("validation_panel_" + item[0], item[1]), validation_status_message.items()))

    except BaseException:
        panel_info = None

    return panel_info if panel_info else {}
