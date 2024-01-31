from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from .forms import LoginForm, RegistrationForm, JobForm
from django.shortcuts import render, redirect
from .models import Student, Job, JobApplication
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages

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
    completed_jobs = Job.objects.filter(assigned_to=student, is_completed=True).count
    context = {
        'student': student,
        'completed_jobs': completed_jobs
    }
    return render(request, 'profile.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    student = request.user
    poster = job.poster
    can_apply = False
    user_has_applied = False
    applications = JobApplication.objects.filter(job = job)
    number_of_applications = applications.count
    if not request.user.is_anonymous:
        can_apply = not user_has_applied and student != poster and job.job_type == student.student_type
        user_has_applied = JobApplication.objects.filter(job = job, applicant=student).exists()
    context = {
        'job' : job,
        'student' : student,
        'poster' : poster,
        'can_apply' : can_apply,
        'number_of_applications': number_of_applications,
        'user_has_applied' : user_has_applied,
        'applications' : applications
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
            if request.user.balance >= job.compensation:
                request.user.balance = request.user.balance -  job.compensation
                request.user.save()
                job.save()
                return redirect('jobs:jobs')
            else:
                messages.error(request, 'Insufficient funds to post the job.')
    else:
        form = JobForm()
    
    return render(request, 'create_job.html', {'form': form, 'student': request.user})

@login_required
def my_jobs(request):
    student = request.user
    assigned_jobs_active = Job.objects.filter(assigned_to=student, is_completed=False)
    posted_jobs_active = Job.objects.filter(poster=student, is_completed=False)
    assigned_jobs_previous = Job.objects.filter(assigned_to=student, is_completed=True)
    posted_jobs_previous = Job.objects.filter(poster=student, is_completed=True)
    context = {
        'student': student, 
        'assigned_jobs_active': assigned_jobs_active,
        'posted_jobs_active': posted_jobs_active,
        'posted_jobs_previous': posted_jobs_previous,
        'assigned_jobs_previous': assigned_jobs_previous
        }
    return render(request, 'my_jobs.html', context)

@require_POST
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    student = request.user
    if student != job.poster and not JobApplication.objects.filter(job=job, applicant=student).exists():
        application = JobApplication.objects.create(job=job, applicant=student)
        response_data = {'success': True, 'message': 'Application submitted successfully!'}
    else:
        response_data = {'success': False, 'message': 'You cannot apply for this job.'}
    return JsonResponse(response_data)


def mark_job_completed(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if(job.is_completed is False):
        request.user.balance += job.compensation
    finished_link = request.POST.get("jobFinishedLink", 'no link provided').strip()
    job.finished_link = finished_link
    job.is_completed = True
    job.save()
    request.user.save()
    return redirect('jobs:job_detail', job_id=job_id)

@require_POST
def accept_job_application(request, application_id):
    application = get_object_or_404(JobApplication, pk=application_id)
    job = application.job
    job.assigned_to = application.applicant
    job.save()
    return redirect('jobs:job_detail', job_id=job.job_id)