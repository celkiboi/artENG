from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student

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