from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from .forms import LoginForm, RegistrationForm, JobForm
from django.shortcuts import render, redirect
from .models import Student, Job
from django.contrib.auth.decorators import login_required

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


def homepage(request):
    student = request.user
    return render(request, 'home.html', {'student': student})

def logout_view(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form, 'student': request.user})

def profile(request, username):
    student = get_object_or_404(Student, user_name=username)
    context = {
        'student': student 
    }
    return render(request, 'profile.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    poster = job.poster
    context = {
        'job' : job,
        'student' : request.user,
        'poster' : poster
    }
    return render(request, 'job_details.html', context)

def jobs(request):
    avalible_jobs = Job.objects.filter(assigned_to__isnull=True)[:5]
    context = {
        'jobs': avalible_jobs,
        'student': request.user
    }
    return render(request, 'jobs.html', context)

@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.poster = request.user  
            if (request.user.student_type == 'engineering'):
                job.job_type = 'art'
            else:
                job.job_type = 'engineering'
            job.save()
            return redirect('jobs:jobs')  
    else:
        form = JobForm()
    
    return render(request, 'create_job.html', {'form': form, 'student': request.user})

@login_required
def my_jobs(request):
    student = request.user
    assigned_jobs = Job.objects.filter(assigned_to=student)
    posted_jobs = Job.objects.filter(poster=student)
    context = {
        'student': student, 
        'assigned_jobs': assigned_jobs,
        'posted_jobs': posted_jobs
        }
    return render(request, 'my_jobs.html', context)