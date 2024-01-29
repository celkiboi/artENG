from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, UserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.
class CustomStudentManager(UserManager):
    def _create_user(self, email, user_name, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  

        return user
    
    def create_user(self, email=None, user_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, user_name, password, **extra_fields)
    
    def create_superuser(self, email=None, user_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, user_name, password, **extra_fields)



class Student(AbstractBaseUser, PermissionsMixin):
    TYPE_CHOICES = (
        ('art', 'Art Student'),
        ('engineering', 'Engineering Student'),
    )
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=20, unique=True)
    
    USERNAME_FIELD = 'user_name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    institution = models.CharField(max_length=6)
    student_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    objects = CustomStudentManager()

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def get_full_name(self):
        return self.user_name
    
    def get_short_name(self):
        return self.user_name

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_student_type_display()})"

