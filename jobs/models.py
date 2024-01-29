from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Student(AbstractUser):
    TYPE_CHOICES = (
        ('art', 'Art Student'),
        ('engineering', 'Engineering Student'),
    )
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='student_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='student_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    student_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    institution = models.CharField(max_length=6)
    student_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.get_student_type_display()})"

class Admin(models.Model):
    TYPE_CHOICES = (
        ('art', 'Art Admin'),
        ('engineering', 'Engineering Admin'),
    )

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    admin_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.get_admin_type_display()})"

