# Django Imports
from django.urls import path

# Model Imports
from expenses import views


urlpatterns = [
    path(
        "periods/",
        views.PeriodListView.as_view(),
        name="period-list",
    ),
    path(
        "list/period/<int:period_id>",
        views.ExpenseListView.as_view(),
        name="expense-list",
    ),
    path(
        "upload/",
        views.UploadExpenseView.as_view(),
        name="expense-upload",
    ),
]