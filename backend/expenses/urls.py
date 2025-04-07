from django.urls import path
from .views import *

urlpatterns = [
    path("", home_view, name="home"),
    path("add/", add_expense, name="add_expense"),
    path("update/<int:id>",update,name="update_expense"),
    path("remove/<int:id>",remove,name="delete_expense"),
    path("upload_expenses/", upload_expenses, name="upload_expenses"),
    path("review/", review_expenses, name="review_expenses"),
    path("save/", save_expenses, name="save_expenses"),
]
