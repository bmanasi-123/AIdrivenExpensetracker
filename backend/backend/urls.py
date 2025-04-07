# import requests
# from django.http import JsonResponse, HttpResponse
from django.urls import path, include
from django.contrib import admin
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", welcome, name="welcome"),
    path("signup/", signupView, name="signup"),
    path("login/", loginView, name="login"),
    path("home/", homeView, name="home"),
    path("home/expenses/", include("expenses.urls")),
    path("home/logout/",logoutView,name='logout'),
]
