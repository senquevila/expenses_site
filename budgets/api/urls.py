# Django Imports
from django.urls import path

# DRF imports
from rest_framework.routers import DefaultRouter

# Model Imports
from budgets.api import views as api_views
from django.urls import include


router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path(
        "expense_not_included/",
        api_views.ExpenseNotIncludedView.as_view(),
        name="expense-not-included",
    )
]
