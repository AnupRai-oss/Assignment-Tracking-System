from rest_framework import serializers
from .models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Assignment.Status.choices)

    class Meta:
        model = Assignment
        fields = [
            "id",
            "title",
            "course",
            "subject_teacher",
            "description",
            "due_date",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]