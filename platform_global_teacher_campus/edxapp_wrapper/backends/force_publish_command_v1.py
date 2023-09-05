"""
Backend for Force Publish Course Command.
"""

from cms.djangoapps.contentstore.management.commands.force_publish import Command

def get_force_publish_course_command():
    """
    Gets force publish course command class from edxapp.
    """

    return Command
