Platform Global Teacher Campus Plugin
######################################

|ci-badge| |codecov-badge| |pyversions-badge| |django-badge|
|license-badge| |status-badge|

This plugin is a Django App for Open edX that adds functionalities to Unesco's Open edX instance.


Functionalities
***************

* Adds the models and their table in the Django Admin page:

  * CourseCategory

  * ValidationBody

  * ValidationProcess

  * ValidationRejectionReason

  * ValidationProcessEvent

  * ValidationRules

  * ValidationStatusMessage

* Adds API methods
  * `Default Router <https://www.django-rest-framework.org/api-guide/routers/#defaultrouter>`_ for categories (But only allows the GET methods)

  * `Default Router <https://www.django-rest-framework.org/api-guide/routers/#defaultrouter>`_ for validation bodies (But only allows the GET methods)

  * POST Validation process to create a validation process

    * validation-processes/<str:course_id>/submit/

  * POST Validation process to create a new ValidationProcessEvent associated

    * validation-processes/<str:course_id>/update-state/

  * GET validation process with course_id

    * validation-processes/<str:course_id>/

  * GET validation process available to see by a user

    * validation-processes/

  * GET user information

    * user-info/

  * GET rejection reasons

    * rejection-reasons/

* Adds filters

  * StopForcePublishCourseRender

  * ModifyRequestToBlockCourse

* Adds a context processor to have the status messages in Studio


Getting Started
***************

Using `Tutor <https://docs.tutor.overhang.io/index.html>`_ as a tool to deploy an instance with this plugin, you only need to add it to the config.yml file in the OPENEDX_EXTRA_PIP_REQUIREMENTS variable:

.. code-block::

  OPENEDX_EXTRA_PIP_REQUIREMENTS:
  - "git+https://github.com/eduNEXT/platform-global-teacher-campus.git"



**NOTE:** If you want to be more specific with the version, you can use something like this:
"git+https://github.com/eduNEXT/platform-global-teacher-campus.git@main#egg=platform-global-teacher-campus==0.1.0"

Save the configuration with Tutor:

.. code-block::

  tutor config save

Build the image:

.. code-block::

  tutor images build openedx

And launch the environment:

.. code-block::

  tutor local launch

Configuration to add
=====================

For the functionality that prevents the publication of courses to work well, you must add their activation to the Studio configuration.
If you are using `eox-tenant <https://github.com/eduNEXT/eox-tenant>`_, create or edit the tenant config for Studio and add the following:

.. code-block::

  {
  "EDNX_USE_SIGNAL": true,
  "OPEN_EDX_FILTERS_CONFIG": {
        "org.openedx.studio.contentstore.modify_usage_key_request.started.v1": {
            "fail_silently": false,
            "pipeline": [
                "platform_global_teacher_campus.filters.pipeline.ModifyRequestToBlockCourse"
            ]
        },
        "org.openedx.studio.manages.force_publish.render.started.v1": {
            "fail_silently": false,
            "pipeline": [
                "platform_global_teacher_campus.filters.pipeline.StopForcePublishCourseRender"
            ]
        }
    }
  }


Compatibility Notes
********************
It is compatible with the Olive release of Open edX.

Getting Help
************

* To report a bug or ask for a feature, go to the Platform Global Teacher Campus Plugin GitHub issues: https://github.com/eduNEXT/platform-global-teacher-campus/issues


License
*******

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.


.. |ci-badge| image:: https://github.com/eduNEXT/platform-global-teacher-campus/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/eduNEXT/platform-global-teacher-campus/actions
    :alt: CI

.. |codecov-badge| image:: https://codecov.io/github/eduNEXT/platform-global-teacher-campus/coverage.svg?branch=main
    :target: https://codecov.io/github/eduNEXT/platform-global-teacher-campus?branch=main
    :alt: Codecov

.. |pyversions-badge| image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://github.com/eduNEXT/platform-global-teacher-campus
    :alt: Supported Python versions

.. |django-badge| image:: https://img.shields.io/badge/django-3.2 | 4.0-blue.svg
    :target: https://github.com/eduNEXT/platform-global-teacher-campus
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/platform-global-teacher-campus.svg
    :target: https://github.com/eduNEXT/platform-global-teacher-campus/blob/main/LICENSE.txt
    :alt: License

.. TODO: Choose one of the statuses below and remove the other status-badge lines.
.. |status-badge| image:: https://img.shields.io/badge/Status-Experimental-yellow
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Deprecated-orange
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Unsupported-red
