from django.contrib import admin
from .models import ValidationBody, CourseCategory, ValidationProcess, ValidationRejectionReason, ValidationProcessEvent, ValidationRules 


class ValidationBodyAdmin(admin.ModelAdmin):
    raw_id_fields = ('validators', 'organizations', )


class ValidationProcessEventAdmin(admin.ModelAdmin):
    raw_id_fields = ('validation_process', 'user', )


class ValidationProcessAdmin(admin.ModelAdmin):
    raw_id_fields = ('course', 'organization', 'current_validation_user', 'validation_body', )


class ValidationRulesAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'validation_body', 'organization', )


class CourseCategoryAdmin(admin.ModelAdmin):
    raw_id_fields = ('parent_category', )


admin.site.register(ValidationBody, ValidationBodyAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(ValidationProcess, ValidationProcessAdmin)
admin.site.register(ValidationRejectionReason)
admin.site.register(ValidationProcessEvent, ValidationProcessEventAdmin)
admin.site.register(ValidationRules, ValidationRulesAdmin)
