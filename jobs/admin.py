from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Job, JobApplication, Dispute

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

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'applied_at', 'is_accepted')
    list_filter = ('is_accepted',)
    search_fields = ('job__name', 'applicant__user_name', 'applicant__first_name', 'applicant__last_name')
    date_hierarchy = 'applied_at'

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'chosen_side', 'eng_approved', 'art_approved')
    search_fields = ('id', 'job', 'chosen_side', 'eng_approved', 'art_approved')