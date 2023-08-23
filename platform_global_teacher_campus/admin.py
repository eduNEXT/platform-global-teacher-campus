from django.contrib import admin
from .models import ValidationBody, CourseCategory, ValidationProcess, ValidationRejectionReason, ValidationProcessEvent, ValidationRules 

admin.site.register(ValidationBody)
admin.site.register(CourseCategory)
admin.site.register(ValidationProcess)
admin.site.register(ValidationRejectionReason)
admin.site.register(ValidationProcessEvent)
admin.site.register(ValidationRules)