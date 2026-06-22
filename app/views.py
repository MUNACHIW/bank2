from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()
# Create your views here.
def landing(request):
    return render(request, "app/index.html")

def login(request):
    return render(request, "app/login.html")

def signup(request):

    if request.method == "POST":

        first_name = request.POST.get("firstName")
        middle_name = request.POST.get("middleName")
        last_name = request.POST.get("lastName")
        username = request.POST.get("username")

        email = request.POST.get("email")
        phone = request.POST.get("phone")
        country = request.POST.get("country")

        account_type = request.POST.get("accountType")
        currency = request.POST.get("currency")

        pin = request.POST.get("pin")

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("/signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("/signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("/signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.middle_name = middle_name
        user.phone = phone
        user.country = country
        user.account_type = account_type
        user.currency = currency
        user.pin = pin

        user.save()

        messages.success(request, "Account created successfully.")

        return redirect("/login")

    return render(request, "app/signup.html")

def personal(request):
    return render(request , "app/personal.html")

def cooperate(request):
    return render(request , "app/cooperate.html")

def insurance(request):
    return render(request,"app/insurance.html")

def mortgage(request):
    return render(request,"app/mortgage.html")
def terms(request):
    return render(request, "app/terms.html")

def contact(request):
    return render(request, "app/contact.html")
def card(request):
    return render(request, "app/credit.html")
def savings(request):
    return render(request, "app/savings.html")
def busloans(request):
    return render(request, "app/business.html")
def about(request):
    return render(request, 'app/about.html')