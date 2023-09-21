"""
Database models for platform_global_teacher_campus.
"""

from django.db import models
from platform_global_teacher_campus.edxapp_wrapper.courses import get_course_overview
from platform_global_teacher_campus.edxapp_wrapper.users import get_user_model
from platform_global_teacher_campus.edxapp_wrapper.organizations import get_organization_model
from platform_global_teacher_campus.edxapp_wrapper.course_roles import get_course_staff_role
from platform_global_teacher_campus.edxapp_wrapper.course_access_role import get_course_access_role

CourseOverview = get_course_overview()
User = get_user_model()
Organization = get_organization_model()
CourseStaffRole = get_course_staff_role()
CourseAccessRole = get_course_access_role()


class CourseCategory(models.Model):
    name = models.TextField()
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.parent_category:
            return f"{self.name} (Parent: {self.parent_category})"
        return self.name

    class Meta:
        verbose_name_plural = "Course Categories"


class ValidationBody(models.Model):
    validators = models.ManyToManyField(User, related_name="validation_bodies")
    name = models.TextField()
    admin_notes = models.TextField(default="")
    organizations = models.ManyToManyField(Organization)

    def __str__(self):
        return self.name

    def is_validator(self, user):
        user = user if isinstance(user, User) else User.objects.get(id=user)
        return user in self.validators.all()

    class Meta:
        verbose_name_plural = "Validation Bodies"


class ValidationProcess(models.Model):
    course = models.OneToOneField(CourseOverview, on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField(CourseCategory)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    current_validation_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    validation_body = models.ForeignKey(ValidationBody, on_delete=models.SET_NULL, null=True)

    @classmethod
    def get_from_course_id(cls, course_id):
        try:
            return cls.objects.get(course_id=course_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def can_user_submit(cls, user, course_id):
        if not isinstance(user, User):
            user = User.objects.get(id=user)

        course = CourseOverview.objects.get(id=course_id)
        if course:
            return CourseStaffRole(course.id).has_user(user)
        return False

    def is_validator(self, user):
        user_id = user.id if isinstance(user, User) else user
        return self.current_validation_user == user_id or self.validation_body.is_validator(user)

    def __str__(self):
        return f"Validation Process for Course {self.course}"

    class Meta:
        verbose_name_plural = "Validation Processes"


class ValidationRejectionReason(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Validation Rejection Reasons"


class ValidationProcessEvent(models.Model):
    class StatusChoices(models.TextChoices):
        SUBMITTED = "subm", "Submitted"
        IN_REVIEW = "revi", "In Review"
        DRAFT = "drft", "Draft"
        APPROVED = "aprv", "Approved"
        DISAPPROVED = "dprv", "Disapproved"
        CANCELLED = "cncl", "Cancelled"
        EXEMPT = "exmp", "Exempt"

    class RoleChoices(models.TextChoices):
        BETA = "beta", "beta"
        INSTRUCTOR = "instructor", "instructor"
        STAFF = "staff", "staff"
        LIMITED_STAFF = "limited_staff", "limited_staff"
        CCX_COACH = "ccx_coach", "ccx_coach"
        DATA_RESEARCHER = "data_researcher", "data_researcher"

    validation_process = models.ForeignKey(
        ValidationProcess,
        on_delete=models.SET_NULL,
        null=True,
        related_name="events"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=5, choices=StatusChoices.choices, default="subm")
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reason = models.ForeignKey(ValidationRejectionReason, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        status_display = dict(ValidationProcessEvent.StatusChoices.choices).get(self.status, "Unknown")
        return f"Event ({status_display}) for Validation Process (ID: {self.validation_process.id})"

    @classmethod
    def can_user_update_to(cls, user, validation_process, status):
        allowed_status = set()

        if ValidationProcess.can_user_submit(user, validation_process.course.id):
            allowed_status.update([
                cls.StatusChoices.SUBMITTED,
                cls.StatusChoices.CANCELLED
            ])

        if validation_process.is_validator(user):
            allowed_status.update([
                cls.StatusChoices.SUBMITTED,
                cls.StatusChoices.IN_REVIEW,
                cls.StatusChoices.DRAFT,
                cls.StatusChoices.APPROVED,
                cls.StatusChoices.DISAPPROVED,
            ])
            if status == ValidationProcessEvent.StatusChoices.IN_REVIEW:
                CourseAccessRole.objects.create(user=user, course_id=validation_process.course.id, org=validation_process.organization.name, role=cls.RoleChoices.STAFF)
            

        return status in allowed_status

    @classmethod
    def can_transition_from_to(cls, current_status, new_status):
        allowed_transitions = {
            cls.StatusChoices.SUBMITTED: [
                cls.StatusChoices.IN_REVIEW,
                cls.StatusChoices.CANCELLED,
            ],
            cls.StatusChoices.IN_REVIEW: [
                cls.StatusChoices.DRAFT,
                cls.StatusChoices.APPROVED,
                cls.StatusChoices.DISAPPROVED,
            ],
            cls.StatusChoices.DRAFT: [
                cls.StatusChoices.SUBMITTED,
            ],
            cls.StatusChoices.APPROVED: [],
            cls.StatusChoices.DISAPPROVED: [],
            cls.StatusChoices.CANCELLED: [
                cls.StatusChoices.SUBMITTED,
            ],
        }

        return new_status in allowed_transitions.get(current_status, [])

    class Meta:
        verbose_name_plural = "Validation Process Events"


class ValidationRules(models.Model):
    class PermissionTypeChoices(models.TextChoices):
        """
        Org Excluded: No validation process
        Org Exempt: Automatic validation process
        User Exempt by org: Automatic validation process
        Validation Body Exempt by org: Automatic validation process
        """
        ORG_EXCLUDED = "org_excluded", "Organization Excluded"
        ORG_EXEMPT = "org_exempt", "Organization Exempt"
        USER_EXEMPT = "user_exempt", "User Exempt"
        VALIDATION_BODY_EXEMPT = "vb_exempt", "Validation Body Exempt"

    permission_type = models.CharField(max_length=15, choices=PermissionTypeChoices.choices, default="org_excluded")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    validation_body = models.ForeignKey(ValidationBody, on_delete=models.CASCADE, null=True, blank=True)
    admin_notes = models.TextField(default="")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField()

    def __str__(self):
        permission_type_display = dict(ValidationRules.PermissionTypeChoices.choices).get(self.permission_type, "Unknown")

        if self.permission_type in ["org_excluded", "org_exempt"]:
            return f"{permission_type_display} - {self.organization}"

        if self.permission_type == "user_exempt":
            return f"{permission_type_display} - {self.user} in {self.organization}"

        if self.permission_type == "vb_exempt":
            return f"{permission_type_display} - {self.validation_body} in {self.organization}"

    class Meta:
        verbose_name_plural = "Validation Rules"


class ValidationStatusMessage(models.Model):
    """
    Model to define a studio course message by the validation process status.
    """
    validation_process_status = ValidationProcessEvent.StatusChoices.choices
    status = models.CharField(max_length=5, choices=validation_process_status, unique=True)
    message = models.TextField(default="")
    button = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_status_display()
    
    def get_the_status_message_by_course_id(course_id):
        # Info to be returned
        course_status = ""
        status_message = ""
        status_button = False

        validation_process = ValidationProcess.get_from_course_id(course_id)
        if validation_process:
            current_event = validation_process.events.last()
            if current_event:
                course_status = current_event.status
                try:
                    validation_status_message = ValidationStatusMessage.objects.get(status=course_status)
                    status_message = validation_status_message.message
                    status_button = validation_status_message.button
                except ValidationStatusMessage.DoesNotExist:
                    pass

        return {
            "course_status": course_status,
            "status_message": status_message,
            "status_button": status_button
        }
