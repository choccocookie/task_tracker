from django.db import models
from employees.models import Employee


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнена'),
    ]

    title = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    parent_task = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='subtasks',
        blank=True,
        null=True,
        verbose_name='Родительская задача'
    )
    assignee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tasks',
        verbose_name='Исполнитель'
    )
    due_date = models.DateField(verbose_name='Срок')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
