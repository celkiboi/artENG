from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Admin

class StudentAdmin(admin.ModelAdmin):
    TYPE_CHOICES = (
        ('art', 'Art Admin'),
        ('engineering', 'Engineering Admin'),
    )

    list_display = ['name', 'surname', 'email', 'student_type']
    search_fields = ['name', 'surname', 'email']
    list_filter = ['student_type']

    def __str__(self):
        return f"{self.username} ({self.get_admin_type_display()})"

admin.site.register(Student, StudentAdmin)

class AdminAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'email', 'admin_type']
    search_fields = ['name', 'surname', 'email']
    list_filter = ['admin_type']

admin.site.register(Admin, AdminAdmin)