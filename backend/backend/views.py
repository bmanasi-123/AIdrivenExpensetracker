from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import CustomUser, LoginDetails
from django.contrib import messages
from django.db.models import Q



def welcome(request):
    """Renders the home page with signup/login modals"""
    return render(request, "welcome.html")


def signupView(request):
    """Handles signup form submission"""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        # first_name = request.POST.get("first_name", "").strip()
        # last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        monthly_budget = request.POST.get("monthly_budget", "0").strip()
        currency = request.POST.get("currency", "INR").strip()

        if not username:
            return render(request, "newuser.html", {"signup_error": "Username is required!"})

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")
            # return render(request, "welcome.html", {"signup_error": "Username already exists"})

        if CustomUser.objects.filter(Q(phone_number=phone_number) | Q(email=email)).exists():
            messages.error(request, "An account with this phone number or email already exists. Please login.")
            return redirect("signup")  

            # return render(request, "welcome.html", {"signup_error": "An account with this phone number or email already exists. Please login."})


        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            # first_name=first_name,
            # last_name=last_name,
            email=email,
            phone_number=phone_number,
            monthly_budget=monthly_budget,
            currency=currency
        )

        # LoginDetails.objects.create(user=user, username=username, password=make_password(password))

        messages.success(request, "Signup successful! Please Login.")
        return redirect('/login')

    return render(request, "signup.html")


def loginView(request):
    """Handles login form submission"""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/home")  
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
            # return render(request, "welcome.html", {"login_error": "Invalid credentials"})

    return render(request, "login.html")

def homeView(request):
    """Renders the home page with user-specific data"""
    # if not request.user.is_authenticated:
    #     return redirect("welcome")

    return render(request, "home.html", {"user": request.user})

def logoutView(request):
    logout(request)
    return redirect("login")