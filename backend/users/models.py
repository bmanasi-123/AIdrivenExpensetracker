from django.contrib.auth.models import AbstractUser
from django.db import models


# class CustomUser(AbstractUser):
#     """
#     Extends Django's default user model to store additional user data.
#     Fixes clashes by adding `related_name` to `groups` and `user_permissions`.
#     """
#     phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)  # For SMS alerts
#     monthly_budget = models.FloatField(default=0.0)  # Used to trigger overspending alerts
#     currency = models.CharField(max_length=5, default="INR")  # Supports multi-currency (e.g., USD, EUR)
#     alert_threshold = models.FloatField(default=80.0)  # Triggers an alert when 80% of budget is spent
#     preferred_alerts = models.CharField(
#         max_length=10,
#         choices=[("SMS", "SMS"), ("Email", "Email"), ("Both", "Both")],
#         default="Both"
#     )  # Defines preferred method of receiving spending alerts
#
#     # ✅ Fixes E304 error by defining custom related_name for groups & permissions
#     groups = models.ManyToManyField(
#         "auth.Group",
#         related_name="customuser_groups",
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         "auth.Permission",
#         related_name="customuser_permissions",
#         blank=True
#     )
#
#     def __str__(self):
#         return self.username


# class CustomUser(AbstractUser):
#     phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional field
#     budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional
#
#     def __str__(self):
#         return self.username

