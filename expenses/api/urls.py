# Django Imports
from django.urls import path

# DRF imports
from rest_framework.routers import DefaultRouter

# Model Imports
from expenses import api as api_views


router = DefaultRouter()
router.register(r"expenses", api_views.ExpenseViewSet, basename="expenses")
urlpatterns = router.urls

urlpatterns = [
    path(
        "currency/converts/",
        api_views.CurrencyConvertViewSet.as_view({"get": "list"}),
        name="currency-convert",
    ),
    path(
        "currency/create_usd_exchange/",
        api_views.CreateDollarConvertionView.as_view(),
        name="create-dollar-convert",
    ),
    path(
        "expense/<int:period>/summary/",
        api_views.ExpenseSummaryListView.as_view(),
        name="expense-summary-list",
    ),
]
