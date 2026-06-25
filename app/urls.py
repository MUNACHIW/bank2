from django.urls import path
from . import views
from .views_pin import verify_pin
app_name = "app"
urlpatterns = [
    path(
        "", views.landing, name="landing"
    ),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('wire-transfer/',     views.wire_transfer,     name='wire_transfer'),
     path('domestic-transfer/', views.domestic_transfer, name='domestic_transfer'),
     path('transactions/', views.transactions, name='transactions'),
     path('dashloans',  views.loans, name="dashloans"),
     path('profile/',       views.profile_view,  name='profile'),
     path('settings/',      views.settings_view, name='settings'),
      path('notifications/', views.notifications, name='notifications'),
     path("personal/", views.personal, name="personal"),
    path("cooperate/", views.cooperate, name='cooperate'),
    path("insurance/", views.insurance, name="insurance"),
    path("mortgage/", views.mortgage, name="mortgage"),
    path("terms/", views.terms,name="name" ),
     path("contact/", views.contact,name="contact" ),
       path("card/", views.card,name="contact" ),
        path("savings/", views.savings,name="savings" ),
        path("loans/", views.busloans, name="loans"),
         path('deposits/',      views.deposits,      name='deposits'),
        path("about/", views.about , name="about"),
         path('transfer/receipt/<str:transfer_type>/<int:transfer_id>/',
     views.transfer_receipt,
     name='transfer_receipt'),
          path('verify-pin/',   verify_pin,  name='verify_pin'),
            path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

]
