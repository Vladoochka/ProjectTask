from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Customer, Employee, Task


class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'full_name', 'email', 'phone', 'role']
    list_filter = ['role']
    search_fields = ['username', 'full_name', 'email', 'phone']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email', 'phone', 'role')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'full_name', 'email', 'phone', 'role'),
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Task)
