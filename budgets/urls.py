from django.urls import path
from .views import (
    CategoryCreateView,
    CategoryUpdateView,
    BudgetCreateView,
    BudgetUpdateView,
    BudgetAssignmentCreateView,
    BudgetAssignmentUpdateView,
)

urlpatterns = [
    path("category/add/", CategoryCreateView.as_view(), name="category-add"),
    path("category/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category-edit"),
    path("budget/add/", BudgetCreateView.as_view(), name="budget-add"),
    path("budget/<int:pk>/edit/", BudgetUpdateView.as_view(), name="budget-edit"),
    path(
        "assignment/add/",
        BudgetAssignmentCreateView.as_view(),
        name="budget-assignment-add",
    ),
    path(
        "assignment/<int:pk>/edit/",
        BudgetAssignmentUpdateView.as_view(),
        name="budget-assignment-edit",
    ),
]
