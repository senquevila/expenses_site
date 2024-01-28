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
        "create_usd_exchange/",
        api_views.CreateDollarConversionView.as_view(),
        name="create-dollar-convert",
    ),
    path(
        "account_assoc/",
        api_views.AccountAssociationView.as_view(),
        name="account-assoc",
    ),
    path(
        "upload_file_cleanup/",
        api_views.ExpenseUploadFileCleanupView.as_view(),
        name="upload-file-cleanup"
    ),
]
