from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.core.validators import FileExtensionValidator
from django.db.models.base import Model
from django.forms.utils import ErrorList

from expenses.models import Account, Transaction, Upload


class AccountTransferForm(forms.Form):
    account_origin = forms.ModelChoiceField(queryset=Account.objects.order_by("name"))
    account_destination = forms.ModelChoiceField(
        queryset=Account.objects.order_by("name")
    )

    def clean(self):
        cleaned_data = super().clean()
        account_origin = cleaned_data.get("account_origin")
        account_destination = cleaned_data.get("account_destination")

        if account_origin == account_destination:
            raise forms.ValidationError("Accounts cannot be the same")

        return cleaned_data


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "description",
            "payment_date",
            "period",
            "account",
            "currency",
            "amount",
        ]


class TransactionUploadForm(forms.Form):
    file = forms.FileField(
        label="Archivo",
        help_text="Seleccione un archivo CSV para cargar",
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
    )

    class Meta:
        model = Transaction
        fields = (
            "periodo",
            "description",
            "payment_date",
            "account",
            "currency",
            "amount",
            "created",
        )


class TransactionInspectionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ("account",)


class UploadForm(forms.ModelForm):
    file = forms.FileField(
        label="Archivo",
        help_text="Seleccione un archivo CSV para cargar",
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
    )

    class Meta:
        model = Upload
        fields = ("file",)


class UploadTransformForm(forms.ModelForm):
    start_row = forms.IntegerField(
        label="Start row",
        help_text="File number where the data starts",
        initial=2,
    )
    end_row = forms.IntegerField(
        label="End row",
        help_text="File number where the data ends",
        initial=0,
    )
    payment_date = forms.IntegerField(label="Payment date", required=False)
    description = forms.IntegerField(label="Description", required=False)
    amount = forms.IntegerField(label="Amount", required=False)
    amount_currency = forms.IntegerField(label="Dollar amount", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _fields = [
            "payment_date",
            "description",
            "amount",
            "amount_currency",
            "start_row",
            "end_row",
        ]

        for field in _fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    class Meta:
        model = Upload
        fields = ("parameters",)
