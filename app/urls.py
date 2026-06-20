from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    path(
        "", views.landing, name="landing"
    ),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup")
    
    
    
]
