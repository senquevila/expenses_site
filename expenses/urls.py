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
        "period_close/<int:pk>/",
        views.PeriodCloseView.as_view(),
        name="period-close",
    ),
    path(
        "expenses/<int:period>/<int:account>",
        views.ExpenseListView.as_view(),
        name="expense-list",
    ),
    path(
        "periods/<int:period>",
        views.ExpenseGroupListView.as_view(),
        name="period-expense-group",
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
