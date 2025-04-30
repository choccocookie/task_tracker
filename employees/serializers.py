from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeWorkLoadSerializer(serializers.ModelSerializer):
    active_tasks_count = serializers.IntegerField()

    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'position', 'active_tasks_count']
