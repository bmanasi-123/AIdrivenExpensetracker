from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import LoginDetails


def welcome(request):
    """Renders the home page with signup/login modals"""
    return render(request, "welcome.html")


def SignupView(request):
    """Handles signup form submission"""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "welcome.html", {"signup_error": "Username already exists"})

        user = CustomUser.objects.create_user(username=username, password=password)
        LoginDetails.objects.create(user=user, username=username, password=password)  # Store in LoginDetails
        return redirect("welcome")

    return redirect("welcome")


def LoginView(request):
    """Handles login form submission"""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("welcome")  # Redirect to home page after login
        else:
            return render(request, "welcome.html", {"login_error": "Invalid credentials"})

    return redirect("welcome")
