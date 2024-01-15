from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from budgets.models import Category, Budget, BudgetAssignment
from budgets.forms import CategoryForm, BudgetForm, BudgetAssignmentForm


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "budgets/category_form.html"
    success_url = reverse_lazy("category-list")  # Replace with the actual URL


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "budgets/category_form.html"
    success_url = reverse_lazy("category-list")


class CategoryListView(ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"


class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = "budgets/budget_form.html"
    success_url = reverse_lazy("budget-list")


class BudgetUpdateView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = "budgets/budget_form.html"
    success_url = reverse_lazy("budget-list")


class BudgetListView(ListView):
    model = Budget
    template_name = "budget_list.html"
    context_object_name = "budgets"


class BudgetAssignmentCreateView(CreateView):
    model = BudgetAssignment
    form_class = BudgetAssignmentForm
    template_name = "budgets/budget_assignment_form.html"
    success_url = reverse_lazy("budget-assignment-list")


class BudgetAssignmentUpdateView(UpdateView):
    model = BudgetAssignment
    form_class = BudgetAssignmentForm
    template_name = "budgets/budget_assignment_form.html"
    success_url = reverse_lazy("budget-assignment-list")


class BudgetAssignmentListView(ListView):
    model = BudgetAssignment
    template_name = "budget_assignment_list.html"
    context_object_name = "budget_assignments"
