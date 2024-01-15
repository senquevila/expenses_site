from rest_framework import serializers
from .models import Category, Budget, BudgetAssignment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = "__all__"


class BudgetAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetAssignment
        fields = "__all__"
