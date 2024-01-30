from django.urls import path
from .views import homepage, logout_view, profile
from .views import CustomLoginView, register

app_name = "jobs"
urlpatterns = [
    path('', homepage, name="home"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('profile/<str:username>', profile, name='profile'),
]
