from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .models import Employee
from .serializers import EmployeeSerializer, EmployeeWorkLoadSerializer
from .paginators import StandardResultsSetPagination
from django.db.models import Count, Q


class EmployeeCreateView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeListView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = StandardResultsSetPagination


class EmployeeRetrieveView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeUpdateView(UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDestroyView(DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeWorkLoadView(ListAPIView):
    serializer_class = EmployeeWorkLoadSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Employee.objects.annotate(
            active_tasks_count=Count(
                'tasks',
                filter=Q(tasks__status__in=['new', 'in_progress'])
            )
        ).order_by('-active_tasks_count')
