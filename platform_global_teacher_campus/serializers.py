from rest_framework import serializers
from .models import ValidationBody

class ValidationBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationBody
        fields = '__all__'
