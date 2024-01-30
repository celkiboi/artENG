from django.urls import path
from .views import homepage, logout_view, profile, job_detail, jobs, create_job, my_jobs
from .views import CustomLoginView, register

app_name = "jobs"
urlpatterns = [
    path('', homepage, name="home"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('profile/<str:username>', profile, name='profile'),
    path('jobs/<int:job_id>', job_detail, name='job_detail'),
    path('jobs/', jobs, name="jobs"),
    path('jobs/create', create_job, name='create_job'),
    path('jobs/my', my_jobs, name='my_jobs')
]
