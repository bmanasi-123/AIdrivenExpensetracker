from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from expenses.models import Expense
from django.db.models import Sum
from backend.models import CustomUser  
from datetime import datetime
import pandas as pd


@login_required
def home_view(request):
    """Displays homepage with expenses"""
    expenses = Expense.objects.filter(user=request.user).order_by("-created_at")  

    user = request.user  
    print(user)
    monthly_budget = user.monthly_budget  

    # Get total expenses for the current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    total_expenses = Expense.objects.filter(user_id=user.id,  created_at__month=current_month , created_at__year = current_year).aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate remaining budget
    remaining_budget = monthly_budget - total_expenses

    return render(request, "home.html", {
        "expenses": expenses,
        "monthly_budget": monthly_budget,
        "remaining_budget": remaining_budget
    })


@login_required
def add_expense(request):
    """Handles adding a new expense."""
    if request.method == "POST":
        print("DEBUG - request.POST:", request.POST)

        name = request.POST.get("name", "").strip()
        amount = request.POST.get("amount", "").strip()
        category = request.POST.get("category", "").strip()
        date_str = request.POST.get("date", "").strip()

        print(name, amount, category)

        if not name or not amount or not category:
            messages.error(request, "All fields are required.")
            return redirect("home")

        # Convert date to correct format
        expense_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")

        # Save expense to DB
        Expense.objects.create(
            user=request.user,
            name=name,
            amount=float(amount),
            category=category,
            created_at=expense_date
        )

        messages.success(request, "Expense added successfully!")
        return redirect("home")  # Redirect to home page

    return redirect("home")


@login_required()
def update(request, id):
    expense = get_object_or_404(Expense, id=id)  # Get the expense or show 404

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        amount = request.POST.get("amount", "").strip()
        category = request.POST.get("category", "").strip()
        date_str = request.POST.get("date", "").strip()

        try:
            expense_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            messages.error(request, "Invalid date format. Please select a valid date.")
            return redirect("update", id=id)

        # Updating the expense object
        expense.name = name
        expense.amount = amount
        expense.category = category
        expense.created_at = expense_date
        expense.save()  # Save the changes

        messages.success(request, "Expense updated successfully!")
        return redirect("home")  # Redirect to home page

    return render(request, "update.html", {"expense": expense})

@login_required
def remove(request,id):
    expense=Expense.objects.get(id=id)
    expense.delete()
    return redirect("home") 

@login_required
def upload_expenses(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        
        if not uploaded_file:
            messages.error(request, "No file selected!")
            return redirect("home")

        # Check if the file is CSV or Excel
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            messages.error(request, "Invalid file format! Please upload a CSV or Excel file.")
            return redirect("home")

        # Check required columns exist
        required_columns = {"Date", "Description", "Amount" , "Category"}
        if not required_columns.issubset(df.columns):
            messages.error(request, "Missing required columns: Date, Description, Amount, Category")
            return redirect("home")

        # Extract and clean data
        extracted_expenses = []
        for _, row in df.iterrows():
            try:
                expense_date = datetime.strptime(str(row["Date"]), "%Y-%m-%d")
                description = row["Description"].strip()
                amount = float(row["Amount"])
                category = row["Category"].strip()

                extracted_expenses.append({
                    "date": expense_date.strftime("%Y-%m-%d"),
                    "name": description,
                    "amount": amount,
                    "category": category
                })
            except Exception as e:
                print(f"Error processing row: {row}, Error: {e}")

        # Store extracted data in session (temporary storage before saving)
        print("DEBUG - extracted_expenses:", extracted_expenses)
        request.session["extracted_expenses"] = extracted_expenses
        messages.success(request, "File uploaded successfully! Review your extracted expenses.")
        return redirect("review_expenses")

    return redirect("home")

def review_expenses(request):
    extracted_expenses = request.session.get("extracted_expenses", [])
    return render(request, "review_expenses.html", {"extracted_expenses": extracted_expenses})

def save_expenses(request):
    extracted_expenses = request.session.get("extracted_expenses", [])

    if not extracted_expenses:
        messages.error(request, "No expenses to save!")
        return redirect("home")

    for expense_data in extracted_expenses:
        Expense.objects.create(
            user=request.user,
            name=expense_data["name"],
            amount=expense_data["amount"],
            category=expense_data["category"], 
            created_at=expense_data["date"],
        )

    # Clear session data
    del request.session["extracted_expenses"]

    messages.success(request, "Expenses saved successfully!")
    return redirect("home")
