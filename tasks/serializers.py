from rest_framework import serializers
from .models import Task
from .validators import validate_not_self_parent, validate_due_date_not_in_past, \
    validate_due_date_not_later_than_parent


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_due_date(self, value):
        return validate_due_date_not_in_past(value)

    def validate(self, attrs):
        parent_task = attrs.get('parent_task') or (self.instance and self.instance.parent_task)
        due_date = attrs.get('due_date') or (self.instance and self.instance.due_date)

        validate_not_self_parent(self.instance, parent_task)
        validate_due_date_not_in_past(due_date)
        validate_due_date_not_later_than_parent(self.instance, due_date, parent_task)

        return attrs


class ImportantTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    due_date = serializers.DateField()
    available_employees = serializers.ListField(child=serializers.CharField())
