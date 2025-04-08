# import requests
# from django.http import JsonResponse, HttpResponse
from django.urls import path, include
from django.contrib import admin
from .views import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", welcome, name="welcome"),
    path("signup/", signupView, name="signup"),
    path("login/", loginView, name="login"),
    path("home/", homeView, name="home"),
    path("home/expenses/", include("expenses.urls")),
    path("home/logout/",logoutView,name='logout'),
    path("home/profile/", updateProfile, name="profile"),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'), name='reset_password'),

    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        # template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
    template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

