from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .models import Task
from .serializers import TaskSerializer

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
