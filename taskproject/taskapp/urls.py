from django.urls import path
from .views import (
    CurrentUserView,
    CustomerCreateView, CustomerListView,
    EmployeeCreateView, EmployeeListView,
    TaskListCreateView, TaskDetailView, TaskCloseView
)

urlpatterns = [
    path('user/', CurrentUserView.as_view(), name='current_user'),
    path('customers/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/list/', CustomerListView.as_view(), name='customer_list'),
    path('employees/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/list/', EmployeeListView.as_view(), name='employee_list'),
    path('tasks/', TaskListCreateView.as_view(), name='task_list_create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/close/', TaskCloseView.as_view(), name='task_close'),
]
