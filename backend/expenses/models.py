from django.db import models
from backend.models import CustomUser  


class ExpenseCategory(models.TextChoices):
    FOOD = "Food"
    TRAVEL = "Travel"
    SHOPPING = "Shopping"
    ENTERTAINMENT = "Entertainment"
    BILLS = "Bills"
    OTHER = "Other"


class Expense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ForeignKey to CustomUser
    name = models.CharField(max_length=255)  # Expense name
    amount = models.FloatField()  # Expense amount
    category = models.CharField(
        max_length=20, choices=ExpenseCategory.choices
    )  # Enum-like category
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return f"{self.name} - {self.amount} ({self.category})"
