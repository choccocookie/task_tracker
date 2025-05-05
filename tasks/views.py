from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .models import Task
from .serializers import TaskSerializer, ImportantTaskSerializer
from employees.models import Employee
from django.db.models import Q, Count


class TaskCreateView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskListView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRetrieveView(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskUpdateView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDestroyView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ImportantTasksView(ListAPIView):
    serializer_class = ImportantTaskSerializer

    def get_queryset(self):
        # Важные задачи: "new", от которых зависят "in_progress"
        important_tasks = Task.objects.filter(
            status='new',
            parent_task__status='in_progress'
        ).distinct()

        # Загруженность сотрудников
        employee_load = Employee.objects.annotate(
            active_tasks_count=Count('tasks', filter=Q(tasks__status__in=['new', 'in_progress']))
        )

        # Наименее загруженный сотрудник
        least_loaded_employee = (
            employee_load.order_by('active_tasks_count').first()
            if employee_load.exists() else None
        )

        result = []

        for task in important_tasks:
            available_employees = set()

            # Сотрудник, выполняющий родитлеьскую задачу
            dependent_employees = (
                {task.parent_task.assignee} if task.parent_task and task.parent_task.assignee else set()
            )

            for employee in dependent_employees:
                employee_task_count = employee.tasks.filter(status__in=['new', 'in_progress']).count()
                if employee_task_count and employee_task_count <= (least_loaded_employee.active_tasks_count + 2):
                    available_employees.add(employee.full_name)
                    print(available_employees)

            if not available_employees and least_loaded_employee:
                available_employees.add(least_loaded_employee.full_name)
                print(available_employees)

            result.append({
                'id': task.id,
                'title': task.title,
                'due_date': task.due_date,
                'available_employees': list(available_employees)
            })

        return result
