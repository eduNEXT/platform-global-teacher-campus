"""
The unable publish or update module define the exception UnablePublishOrUpdate that is used in openedx-filters.
"""


class UnablePublishOrUpdate(Exception):
    """
    Exception raised in openedx-filters when there is an inability to publish or update a module.

    This exception is raised to indicate issues related to the publishing or updating
    functionality within the openedx-filters module.

    Attributes:
        None

    Usage:
        Raise this exception when there is a specific problem preventing the successful
        publishing or updating of a module in openedx.

    Example:
        raise UnablePublishOrUpdate(message)
    """
