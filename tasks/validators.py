from rest_framework import serializers
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_due_date_not_in_past(due_date):
    if due_date < timezone.now().date():
        raise ValidationError("Срок задачи не может быть в прошлом.")
    return due_date


def validate_not_self_parent(instance, parent_task):
    if parent_task and instance and parent_task == instance:
        raise ValidationError("Задача не может быть родительской сама себе.")


def validate_due_date_not_later_than_parent(instance, due_date, parent_task):
    if parent_task and due_date and parent_task.due_date and due_date > parent_task.due_date:
        raise serializers.ValidationError("Срок подзадачи не может быть позже срока родительской задачи.")
