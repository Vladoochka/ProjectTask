from django.test import TestCase
from .models import User, Customer, Employee, Task


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'full_name': 'Test User',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'role': 'customer'
        }
        self.user = User.objects.create(**self.user_data)

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.full_name, 'Test User')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.phone, '1234567890')
        self.assertEqual(self.user.role, 'customer')

    def test_user_str_method(self):
        self.assertEqual(str(self.user), 'Test User')

    def test_user_verbose_name_plural(self):
        self.assertEqual(str(User._meta.verbose_name_plural), 'Пользователи')


class CustomerModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'full_name': 'Test User',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'role': 'customer'
        }
        self.user = User.objects.create(**self.user_data)
        self.customer = Customer.objects.create(user=self.user)

    def test_customer_creation(self):
        self.assertEqual(self.customer.user.username, 'testuser')

    def test_customer_str_method(self):
        self.assertEqual(str(self.customer), 'Test User')

    def test_customer_verbose_name_plural(self):
        self.assertEqual(str(Customer._meta.verbose_name_plural), 'Заказчики')


class EmployeeModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'full_name': 'Test User',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'role': 'employee'
        }
        self.user = User.objects.create(**self.user_data)
        self.employee = Employee.objects.create(user=self.user, can_access_all_tasks=True)

    def test_employee_creation(self):
        self.assertEqual(self.employee.user.username, 'testuser')
        self.assertTrue(self.employee.can_access_all_tasks)

    def test_employee_str_method(self):
        self.assertEqual(str(self.employee), 'Test User')

    def test_employee_verbose_name_plural(self):
        self.assertEqual(str(Employee._meta.verbose_name_plural), 'Сотрудники')


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testcustomer',
            'full_name': 'Test Customer',
            'email': 'testcustomer@example.com',
            'phone': '1234567890',
            'role': 'customer'
        }
        self.customer_user = User.objects.create(**self.user_data)
        self.customer = Customer.objects.create(user=self.customer_user)

        self.employee_data = {
            'username': 'testemployee',
            'full_name': 'Test Employee',
            'email': 'testemployee@example.com',
            'phone': '9876543210',
            'role': 'employee'
        }
        self.employee_user = User.objects.create(**self.employee_data)
        self.employee = Employee.objects.create(user=self.employee_user)

    def test_task_creation(self):
        task = Task.objects.create(customer=self.customer, employee=self.employee, status='waiting')
        self.assertEqual(task.status, 'waiting')
        self.assertEqual(task.customer.user.full_name, 'Test Customer')
        self.assertEqual(task.employee.user.full_name, 'Test Employee')

    def test_task_save_method(self):
        task = Task.objects.create(customer=self.customer, status='completed', report='Test report')
        self.assertEqual(task.status, 'completed')

        # Test saving with empty report
        task.report = ''
        with self.assertRaises(ValueError):
            task.save()

    def test_task_verbose_name_plural(self):
        self.assertEqual(str(Task._meta.verbose_name_plural), 'Задачи')


