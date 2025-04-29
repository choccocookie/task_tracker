from django.urls import path
from .views import (
    EmployeeCreateView,
    EmployeeListView,
    EmployeeRetrieveView,
    EmployeeUpdateView,
    EmployeeDestroyView,
)

urlpatterns = [
    path('create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('list/', EmployeeListView.as_view(), name='employee-list'),
    path('<int:pk>/', EmployeeRetrieveView.as_view(), name='employee-detail'),
    path('<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('<int:pk>/delete/', EmployeeDestroyView.as_view(), name='employee-delete'),
]
