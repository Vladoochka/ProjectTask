from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer, Employee, Task

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'phone', 'role']


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        customer = Customer.objects.create(user=user)
        return customer


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'can_access_all_tasks', 'photo']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee


class TaskSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.id')
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'customer', 'employee', 'status', 'creation_date', 'update_date', 'completion_date', 'report']
