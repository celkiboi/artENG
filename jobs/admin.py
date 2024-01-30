from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Job

class StudentAdmin(admin.ModelAdmin):
    TYPE_CHOICES = (
        ('art', 'Art Admin'),
        ('engineering', 'Engineering Admin'),
    )

    list_display = ('user_name', 'first_name', 'last_name', 'student_type', 'institution')
    search_fields = ['email']
    list_filter = ['student_type']

    def __str__(self):
        return f"{self.username} ({self.get_admin_type_display()})"

admin.site.register(Student, StudentAdmin)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'name', 'job_type', 'poster', 'assign_deadline', 'completion_deadline', 'assigned_to', 'compensation')
    search_fields = ('name', 'description', 'poster__user_name', 'assigned_to__user_name')
    list_filter = ('job_type', 'assign_deadline', 'completion_deadline', 'assigned_to')