from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('employee', 'Employee'),
    )
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    email = models.EmailField(verbose_name='Электронная почта')
    phone = models.CharField(max_length=15, unique=True, verbose_name='Телефон')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='Роль')
    groups = models.ManyToManyField(Group, related_name='taskapp_user_set', blank=True, verbose_name='Группы')
    user_permissions = models.ManyToManyField(Permission, related_name='taskapp_user_set', blank=True,
                                              verbose_name='Права пользователя')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __str__(self):
        return f"{self.user.full_name}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    can_access_all_tasks = models.BooleanField(default=False, verbose_name='Доступ ко всем задачам')
    photo = models.ImageField(upload_to='employee_photos/', verbose_name='Фотография')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f"{self.user.full_name}"


class Task(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'Ожидает исполнителя'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнена'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Заказчик')
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Сотрудник')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name='Статус')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    completion_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')
    report = models.TextField(blank=True, verbose_name='Отчет')

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.report:
            raise ValueError("Отчет не может быть пустым при закрытии задачи.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f"Задача {self.id} для {self.customer.user.full_name}"
