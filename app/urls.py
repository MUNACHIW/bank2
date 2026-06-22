from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    path(
        "", views.landing, name="landing"
    ),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    
     path("personal/", views.personal, name="personal"),
    path("cooperate/", views.cooperate, name='cooperate'),
    path("insurance/", views.insurance, name="insurance"),
    path("mortgage/", views.mortgage, name="mortgage"),
    path("terms/", views.terms,name="name" ),
     path("contact/", views.contact,name="contact" ),
       path("card/", views.card,name="contact" ),
        path("savings/", views.savings,name="savings" ),
        path("loans/", views.busloans, name="loans"),
        path("about/", views.about , name="about")
]
