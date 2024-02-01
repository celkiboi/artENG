from django.urls import path
from .views import homepage, logout_view, profile, job_detail, jobs, create_job, my_jobs, apply_for_job, mark_job_completed, accept_job_application, update_dispute_view, finish_dispute_view, dispute_view, disputes
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
    path('jobs/my', my_jobs, name='my_jobs'),
    path('jobs/<int:job_id>/apply/', apply_for_job, name='apply_for_job'),
    path('jobs/<int:job_id>/mark_completed/', mark_job_completed, name='mark_job_completed'),
    path('jobs/applications/<int:application_id>/accept/', accept_job_application, name='accept_job_application'),
    path('jobs/<int:job_id>/dispute', dispute_view, name="dispute"),
    path('<int:job_id>/update_dispute/', update_dispute_view, name='update_dispute'),
    path('<int:job_id>/finish_dispute/', finish_dispute_view, name='finish_dispute'),
    path('disputes', disputes, name="disputes")
]
