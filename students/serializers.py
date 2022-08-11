from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.conf import settings
from students.models import Course, Student


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, attrs):

        count = Course.objects.count()
        if count > settings.MAX_COURSES:
            raise ValidationError('Курсов слишком много')
        return super().validate(attrs)
