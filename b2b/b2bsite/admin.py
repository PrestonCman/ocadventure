from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Employee, Company

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'company', 'num_queries')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass

