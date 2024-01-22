# Django Imports
from django.urls import path

# Model Imports
from expenses import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "accounts/",
        views.AccountListView.as_view(),
        name="account-list",
    ),
    path(
        "accounts/transfer/",
        views.AccountTransferView.as_view(),
        name="account-transfer",
    ),
    path(
        "currency/convert/",
        views.CurrencyConvertListView.as_view(),
        name="currency-convert-list",
    ),
    path(
        "expenses/",
        views.ExpenseListView.as_view(),
        name="expense-list",
    ),
    path(
        "expenses/add/",
        views.ExpenseCreateView.as_view(),
        name="expense-add",
    ),
    path(
        "expenses/<int:pk>/edit/",
        views.ExpenseUpdateView.as_view(),
        name="expense-edit",
    ),
    path(
        "expenses/<int:pk>/delete/",
        views.ExpenseDeleteView.as_view(),
        name="expense-delete",
    ),
    path(
        "expenses/upload/",
        views.ExpenseUploadView.as_view(),
        name="expense-upload-start",
    ),
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
        views.ExpenseListPerAccountView.as_view(),
        name="expense-account-list",
    ),
]
