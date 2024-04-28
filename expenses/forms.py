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
        initial=0,
    )
    end_row = forms.IntegerField(
        label="End row",
        help_text="File number where the data ends",
        initial=0,
    )
    payment_date = forms.IntegerField(label="Payment date", initial=0)
    description = forms.IntegerField(label="Description", initial=0)
    amount = forms.IntegerField(label="Amount", initial=0)
    amount_currency = forms.IntegerField(label="Dollar amount", initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _fields = [
            "start_row",
            "end_row",
            "payment_date",
            "description",
            "amount",
            "amount_currency",
        ]

        for field in _fields[:2]:
            self.fields[field].widget.attrs["class"] = "form-control"

        for field in _fields[2:]:
            self.fields[field].widget.attrs["class"] = "form-control repaint-trigger"

    class Meta:
        model = Upload
        fields = ("parameters",)
