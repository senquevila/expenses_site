# Django Imports
from django.urls import path

# Model Imports
from expenses import views


urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path(
        "periods/",
        views.PeriodListView.as_view(),
        name="period-list",
    ),
    path(
        "expenses/period/<int:period>",
        views.ExpenseListView.as_view(),
        name="expense-list",
    ),
    path(
        "expenses/upload/",
        views.UploadExpenseView.as_view(),
        name="expense-upload",
    ),
    path(
        "accounts/",
        views.AccountListView.as_view(),
        name="account-list",
    ),
    path(
        "currency-convert/",
        views.CurrencyConvertListView.as_view(),
        name="currency-convert-list",
    ),
]
