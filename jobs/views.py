from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from .forms import LoginForm, RegistrationForm, JobForm
from django.shortcuts import render, redirect
from .models import Student, Job, JobApplication, Dispute
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseForbidden
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
    dispute = Dispute.objects.filter(job = job).first()
    is_disputed = dispute is not None
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
        'applications' : applications,
        'is_disputed' : is_disputed,
        'dispute': dispute
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
    applications = JobApplication.objects.filter(job=job)
    for application in applications.iterator():
        application.delete()
    return redirect('jobs:job_detail', job_id=job.job_id)

@require_POST
def update_dispute_view(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'User is not a staff member.'})
    chosen_side = request.POST.get("chosen_side")
    approved_by = request.POST.get("approved_by")
    dispute, created = Dispute.objects.get_or_create(job=job)
    if approved_by == "engineering":
        dispute.eng_approved = True
    if approved_by == "art":
        dispute.art_approved = True
    dispute.chosen_side = chosen_side
    dispute.save()
    return JsonResponse({'success': True, 'message': 'Dispute updated successfully.'})

@require_POST
def finish_dispute_view(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'User is not a staff member.'})
    dispute = get_object_or_404(Dispute, job=job)
    if dispute.eng_approved and request.user.student_type == "engineering":
        return JsonResponse({'success': False, 'message': 'User is an engineer, needs to be an artist.'})
    if dispute.art_approved and request.user.student_type == "art":
        return JsonResponse({'success': False, 'message': 'User is an artist, needs to be an engineer.'})
    
    answer = request.POST.get("answer")
    if answer == 'no':
        dispute.art_approved = False
        dispute.eng_approved = False
        dispute.save()
        return JsonResponse({'success': True, 'message': 'Dispute is not resolved.'})
    if answer == 'yes':
        if dispute.chosen_side == "poster":
            job.assigned_to.balance -= job.compensation
            job.assigned_to.save()
            job.poster.balance += job.compensation
            job.poster.save()
        job.was_disputed = True
        job.save()
        dispute.delete()
        return JsonResponse({'success': True, 'message': 'Dispute was resolved.'})
    return JsonResponse({'success': False, 'message': 'Unknown error.'})


@login_required
def dispute_view(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(Job, pk=job_id)
        Dispute.objects.create(job=job)
    return JsonResponse({'success': True, 'message': 'Created dispute.'})

@login_required
def disputes(request):
    student = request.user
    if not student.is_staff:
        return HttpResponseForbidden("Access Forbidden")
    disputes = Dispute.objects.iterator()
    jobs = []
    for dispute in disputes:
        jobs.append(dispute.job)
    context = {
        'jobs': jobs,
        'student': student
    }
    return render(request, 'disputes.html', context)