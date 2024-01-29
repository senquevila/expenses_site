from rest_framework import serializers

from expenses.models import (
    Account,
    AccountAsociation,
    CurrencyConvert,
    Expense,
    Period,
    Upload,
)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        ordering = ["name"]


class AccountAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountAsociation
        fields = "__all__"
        ordering = ["account__name"]


class CurrencyConvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyConvert
        fields = "__all__"


class PeriodSerializer(serializers.ModelSerializer):
    """
    Serializer for the Period model.
    """

    class Meta:
        model = Period
        fields = "__all__"
        ordering = ["-year", "-month"]


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Expense model.
    """

    class Meta:
        model = Expense
        fields = "__all__"


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = "__all__"
