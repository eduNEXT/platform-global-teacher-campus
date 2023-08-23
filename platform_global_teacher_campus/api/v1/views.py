"""
API v1 views.
"""

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from models import CourseCategory, ValidationProcess

def index(request):
    categories = CourseCategory.objects.all()
    response_text = "\n".join([category.name for category in categories])
    return HttpResponse(response_text)

def validation_process_detail(request, process_id):
    validation_process = get_object_or_404(ValidationProcess, id=process_id)
    response_text = f"Validation Process for Course {validation_process.course_id}"
    return HttpResponse(response_text)
