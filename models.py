# from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
# from sqlalchemy.orm import relationship
# # from database import Base
# import enum
#
# class ExpenseCategory(str, enum.Enum):
#     FOOD = "Food"
#     TRAVEL = "Travel"
#     SHOPPING = "Shopping"
#     ENTERTAINMENT = "Entertainment"
#     BILLS = "Bills"
#     OTHER = "Other"
#
# class Expense(Base):
#     __tablename__ = "expenses"
#     __table_args__ = {"schema": "public"}
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("public.backend_customuser.id", ondelete="CASCADE"), nullable=False)
#     name = Column(String, nullable=False)
#     amount = Column(Float, nullable=False)
#     category = Column(Enum(ExpenseCategory, name="expense_category"), nullable=False)
#
#     # Relationship (optional, but useful)
#     user = relationship("User", back_populates="expenses")
#
# # class Expense(Base):
# #     __tablename__ = "expenses"
# #     __table_args__ = {"schema": "public"}
# #
# #     id = Column(Integer, primary_key=True, index=True)
# #     user_id = Column(Integer, ForeignKey("backend_customuser.id"), nullable=False)
# #     name = Column(String, nullable=False)
# #     amount = Column(Float, nullable=False)
# #     category = Column(Enum(ExpenseCategory, name="expense_category"), nullable=False)
