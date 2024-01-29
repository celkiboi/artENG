from django.urls import path
from .views import homepage, logout_view
from .views import CustomLoginView

app_name = "jobs"
urlpatterns = [
    path('', homepage),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', logout_view, name='logout'),
]
