"""
Database models for platform_global_teacher_campus.
"""

from django.db import models
from platform_global_teacher_campus.edxapp_wrapper.courses import get_course_overview
from platform_global_teacher_campus.edxapp_wrapper.users import get_user_model
from platform_global_teacher_campus.edxapp_wrapper.organizations import get_organization_model

CourseOverview = get_course_overview()
User = get_user_model()
Organization = get_organization_model()


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
    validators = models.ManyToManyField(User)
    name = models.TextField()
    admin_notes = models.TextField(default="")
    organizations = models.ManyToManyField(Organization)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Validation Bodies"


class ValidationProcess(models.Model):
    course = models.OneToOneField(CourseOverview, on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField(CourseCategory)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    current_validation_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    validation_body = models.ForeignKey(ValidationBody, on_delete=models.SET_NULL, null=True)

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

    validation_process = models.ForeignKey(
        ValidationProcess,
        on_delete=models.SET_NULL,
        null=True,
        related_name="events"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=5, choices=StatusChoices.choices, default="subm")
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reason = models.ForeignKey(ValidationRejectionReason, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        status_display = dict(ValidationProcessEvent.StatusChoices.choices).get(self.status, "Unknown")
        return f"Event ({status_display}) for Validation Process (ID: {self.validation_process.id})"

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
