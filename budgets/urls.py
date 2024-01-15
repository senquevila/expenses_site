from django.urls import path
from budgets.views import (
    CategoryCreateView,
    CategoryUpdateView,
    CategoryListView,
    BudgetCreateView,
    BudgetUpdateView,
    BudgetListView,
    BudgetAssignmentCreateView,
    BudgetAssignmentUpdateView,
    BudgetAssignmentListView,
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/add/", CategoryCreateView.as_view(), name="category-add"),
    path(
        "categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category-edit"
    ),
    path("budgets/", BudgetListView.as_view(), name="budget-list"),
    path("budgets/add/", BudgetCreateView.as_view(), name="budget-add"),
    path("budgets/<int:pk>/edit/", BudgetUpdateView.as_view(), name="budget-edit"),
    path(
        "assignments/",
        BudgetAssignmentListView.as_view(),
        name="budget-assignment-list",
    ),
    path(
        "assignments/add/",
        BudgetAssignmentCreateView.as_view(),
        name="budget-assignment-add",
    ),
    path(
        "assignments/<int:pk>/edit/",
        BudgetAssignmentUpdateView.as_view(),
        name="budget-assignment-edit",
    ),
]
