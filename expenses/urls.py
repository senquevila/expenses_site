# Django Imports
from django.urls import path

# Model Imports
from expenses import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "periods/",
        views.PeriodListView.as_view(),
        name="period-list",
    ),
    path(
        "periods/<int:period>/",
        views.ExpenseGroupListView.as_view(),
        name="period-expense-group",
    ),
    path(
        "periods/<int:pk>/close/",
        views.PeriodCloseView.as_view(),
        name="period-close",
    ),
    path(
        "periods/<int:pk>/open/",
        views.PeriodOpenView.as_view(),
        name="period-open",
    ),
    path(
        "periods/<int:period>/account/<int:account>/",
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
        "accounts/transfer/",
        views.AccountTransferView.as_view(),
        name="account-transfer"
    ),
    path(
        "currency/convert/",
        views.CurrencyConvertListView.as_view(),
        name="currency-convert-list",
    ),
]
