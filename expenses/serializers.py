from rest_framework import serializers

from expenses.models import Account, CurrencyConvertion, Period, Expense


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        ordering = ['name']


class CurrencyConvertionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyConvertion
        fields = '__all__'


class PeriodSerializer(serializers.Serializer):
    """
    Serializer for the Period model.
    """
    class Meta:
        model = Period
        fields = '__all__'
        ordering = ['-year', '-month']


class ExpenseSerializer(serializers.Serializer):
    """
    Serializer for the Expense model.
    """
    class Meta:
        model: Expense
        fields = '__all__'
