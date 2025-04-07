from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Extends Django's default user model to store additional user data.
    Fixes clashes by adding `related_name` to `groups` and `user_permissions`.
    """
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)  # For SMS alerts
    monthly_budget = models.FloatField(default=0.0)  # Used to trigger overspending alerts
    currency = models.CharField(max_length=5, default="INR")  # Supports multi-currency (e.g., USD, EUR)
    alert_threshold = models.FloatField(default=80.0)  # Triggers an alert when 80% of budget is spent
    preferred_alerts = models.CharField(
        max_length=10,
        choices=[("SMS", "SMS"), ("Email", "Email"), ("Both", "Both")],
        default="Both"
    )
    

    USERNAME_FIELD = "username"  
    REQUIRED_FIELDS = ["email"]  


    groups = models.ManyToManyField(
            "auth.Group",
            related_name="customuser_groups",
            blank=True
        )
    user_permissions = models.ManyToManyField(
            "auth.Permission",
            related_name="customuser_permissions",
            blank=True
        )

    def __str__(self):
        return self.username


class LoginDetails(models.Model):
    """Stores login credentials separately"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="login_details")
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords

    def __str__(self):
        return self.username
