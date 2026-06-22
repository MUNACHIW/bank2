from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(request, "app/index.html")

def login(request):
    return render(request, "app/login.html")

def signup(request):
    return render(request , "app/signup.html")

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