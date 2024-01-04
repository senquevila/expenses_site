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
]
