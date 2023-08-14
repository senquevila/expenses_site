# Django Imports
from django.urls import path

# Model Imports
from expenses import views


urlpatterns = [
    path(
        "",
        views.ExpenseListView.as_view(),
        name="expense-list",
    ),
    path(
        "upload/",
        views.UploadExpenseView.as_view(),
        name="expense-upload",
    ),
]