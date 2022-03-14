from rest_framework import serializers
from ..models.tasks import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'assignment_type', 'assignment_typeset',
                  'client_name', 'assigned_to', 'due_date', 'team']
