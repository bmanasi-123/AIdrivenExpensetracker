from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import CustomUser, LoginDetails
from django.contrib import messages



def welcome(request):
    """Renders the home page with signup/login modals"""
    return render(request, "welcome.html")


def SignupView(request):
    """Handles signup form submission"""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        monthly_budget = request.POST.get("monthly_budget", "0").strip()
        currency = request.POST.get("currency", "INR").strip()

        if not username:
            return render(request, "newuser.html", {"signup_error": "Username is required!"})

        if CustomUser.objects.filter(username=username).exists():
            return render(request, "welcome.html", {"signup_error": "Username already exists"})

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            monthly_budget=monthly_budget,
            currency=currency
        )

        LoginDetails.objects.create(user=user, username=username, password=make_password(password))

        messages.success(request, "Signup successful! Please log in.")
        return redirect("login")

    return render(request, "newuser.html")


def LoginView(request):
    """Handles login form submission"""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("welcome")  # Redirect to home page after login
        else:
            return render(request, "welcome.html", {"login_error": "Invalid credentials"})

    return redirect("welcome")
