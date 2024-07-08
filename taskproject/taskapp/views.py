from rest_framework import status
from django.db import models
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer, Employee, Task
from .serializers import UserSerializer, CustomerSerializer, EmployeeSerializer, TaskSerializer
from django.shortcuts import get_object_or_404


class CurrentUserView(APIView):
    @staticmethod
    def get(request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CanCreateCustomerAndEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_employee


class CustomerCreateView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, CanCreateCustomerAndEmployee]


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmployeeCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, CanCreateCustomerAndEmployee]


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer


class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get_queryset(self):
        user = self.request.user
        if user.is_customer:
            return Employee.objects.all()
        return Employee.objects.none()


class CustomerTaskPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer.user == request.user


class EmployeeTaskPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.employee.user == request.user


class CanModifyTaskWhenWaiting(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.status == 'waiting':
            return True
        return False


class CanModifyTaskInProgress(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.status == 'in_progress':
            return True
        return False


class ReadOnlyIfCompleted(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.status == 'completed':
            return False
        return True


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_customer:
            return Task.objects.filter(customer=user.customer)
        elif user.is_employee:
            return Task.objects.filter(models.Q(employee=user.employee) | models.Q(employee=None))

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.customer == request.user.customer


class IsAssignedEmployeeOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if user.is_employee:
            return obj.employee.user == user or user.employee.can_access_all_tasks

        return False


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnlyIfCompleted, IsAssignedEmployeeOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_customer:
            return Task.objects.filter(customer=user.customer)
        elif user.is_employee:
            if user.employee.can_access_all_tasks:
                return Task.objects.all()
            else:
                return Task.objects.filter(models.Q(employee=user.employee) | models.Q(employee=None))

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
            if task.employee and task.employee.user == self.request.user:
                return [permissions.IsAuthenticated(), CanModifyTaskWhenWaiting()]
            elif task.employee is None:
                return [permissions.IsAuthenticated(), CanModifyTaskWhenWaiting()]

        return super().get_permissions()

    def delete(self, request, *args, **kwargs):
        return Response({'message': 'Удаление задач запрещено.'}, status=status.HTTP_403_FORBIDDEN)


class TaskCloseView(APIView):
    @staticmethod
    def post(request, pk):
        task = Task.objects.get(pk=pk)
        task.status = 'completed'
        task.completion_date = timezone.now()
        task.save()
        return Response({'status': 'Задача выполнена.'})
