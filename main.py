from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
# from models import Expense, ExpenseCategory
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import List
from schemas import *
from sqlalchemy import text

app = FastAPI()


# ✅ Create Expense (POST)
@app.post("/expenses/", response_model=ExpenseResponse)
async def create_expense(expense: ExpenseCreate, db: AsyncSession = Depends(get_db)):
    query = text(
        "INSERT INTO expenses (user_id, name, amount, category) VALUES (:user_id, :name, :amount, :category) RETURNING id, created_at"
    )
    async with db.begin():
        result = await db.execute(query, {
            "user_id": expense.user_id,
            "name": expense.name,
            "amount": expense.amount,
            "category": expense.category
        })
        row = result.fetchone()  # ✅ Fetch a single row

    if not row:
        raise HTTPException(status_code=500, detail="Failed to insert expense")

    return {"id": row.id, **expense.dict(), "created_at": row.created_at}


# ✅ Get All Expenses for a Specific User (GET)
@app.get("/expenses/", response_model=ExpenseListResponse)
async def get_all_expenses(db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM expenses")
    async with db.begin():  # ✅ Correct way to use AsyncSession
        result = await db.execute(query)
        rows = result.fetchall()  # Fetch all rows

    expenses = [ExpenseResponse(**dict(row._mapping)) for row in rows]
    return {"expenses": expenses}


@app.get("/expenses/{user_id}", response_model=ExpenseListResponse)
async def get_expenses_by_user(user_id: int, db=Depends(get_db)):
    # query = "SELECT * FROM expenses WHERE user_id = $1"
    query = text("SELECT * FROM expenses WHERE user_id = :user_id")
    # query = text("""
    #         SELECT id, name, amount, category, created_at
    #         FROM expenses
    #         WHERE user_id = :user_id
    #         ORDER BY created_at DESC
    #         LIMIT 50
    #     """)  # ✅ Fetch only needed columns & limit results
    async with db.begin():
        # rows = await db.execute(query, user_id)
        result = await db.execute(query, {"user_id": user_id})
        rows = result.fetchall()
    expenses = [ExpenseResponse(**dict(row._mapping)) for row in rows]
    return {"expenses": expenses}


# ✅ Update an Expense (PUT)
@app.put("/expenses/{user_id}/{expense_id}")
async def update_expense(
    user_id: int,
    expense_id: int,
    expense_update: ExpenseUpdate,  # Pydantic model for validation
    db: AsyncSession = Depends(get_db)
):
    # ✅ Convert category to Title Case (Handles 'food' → 'Food')
    expense_update.category = expense_update.category.title()
    print(expense_update.category)
    # ✅ Validate category (Prevent invalid categories)
    valid_categories = {"Food", "Travel", "Shopping", "Entertainment", "Bills", "Other"}
    if expense_update.category not in valid_categories:
        raise HTTPException(status_code=400,
                            detail=f"Invalid category '{expense_update.category}'"
                                   f".Allowed: {valid_categories}")
    query = text("""
        UPDATE expenses 
        SET name = :name, amount = :amount, category = :category
        WHERE id = :expense_id AND user_id = :user_id
        RETURNING id, name, amount, category, created_at
    """)

    async with db.begin():
        result = await db.execute(query, {
            "expense_id": expense_id,
            "user_id": user_id,
            "name": expense_update.name,
            "amount": expense_update.amount,
            "category": expense_update.category
        })
        updated_expense = result.fetchone()

    if not updated_expense:
        raise HTTPException(status_code=404, detail="Expense not found or does not belong to user")

    return {"message": "Expense updated successfully", "expense": dict(updated_expense._mapping)}


# ✅ Delete an Expense (DELETE)
@app.delete("/expenses/{user_id}/{expense_id}")
async def delete_expense(user_id: int, expense_id: int, db: AsyncSession = Depends(get_db)):
    query = text("""
        DELETE FROM expenses 
        WHERE id = :expense_id AND user_id = :user_id
        RETURNING id
    """)

    async with db.begin():
        result = await db.execute(query, {"expense_id": expense_id, "user_id": user_id})
        deleted_expense = result.fetchone()

    if not deleted_expense:
        raise HTTPException(status_code=404, detail="Expense not found or does not belong to user")

    return {"message": "Expense deleted successfully"}

