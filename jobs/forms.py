from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Student

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", required=True)

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['email', 'user_name', 'first_name', 'last_name', 'institution', 'student_type', 'password1', 'password2']
