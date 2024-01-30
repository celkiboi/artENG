from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Student, Job

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", required=True)

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['email', 'user_name', 'first_name', 'last_name', 'institution', 'student_type', 'password1', 'password2']

class DateInput(forms.DateInput):
    input_type = 'date'

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['name', 'description', 'assign_deadline', 'completion_deadline', 'compensation']
        widgets = {
            'assign_deadline': DateInput(),
            'completion_deadline': DateInput(),
        }
