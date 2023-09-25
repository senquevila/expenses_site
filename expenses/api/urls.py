# Django Imports
from django.urls import path

# DRF imports
from rest_framework.routers import DefaultRouter

# Model Imports
from expenses import api as api_views
from django.urls import include


router = DefaultRouter()
router.register(r"expenses", api_views.ExpenseViewSet, basename="expenses")
router.register(r"accounts", api_views.AccountViewSet, basename="accounts")
router.register(
    r"currency_converts", api_views.CurrencyConvertViewSet, basename="currency_converts"
)

urlpatterns = [
    path("", include(router.urls)),
    # period
    path(
        "period/close/<int:pk>/",
        api_views.PeriodCloseView.as_view(),
        name="period-close",
    ),
    # currencies
    path(
        "currency/create_usd_exchange/",
        api_views.CreateDollarConvertionView.as_view(),
        name="create-dollar-convert",
    ),
    # account
    path(
        "account/swap/",
        api_views.SwapAccountView.as_view(),
        name="account-swap",
    ),
    # expense
    path(
        "expense/<int:period>/summary/",
        api_views.ExpenseSummaryListView.as_view(),
        name="expense-summary-list",
    ),
]
