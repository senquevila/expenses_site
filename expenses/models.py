from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import F
from django.db.models.functions import Abs
from django.utils import timezone

from expenses.mixins import CreationModificationDateMixin


class Period(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    closed = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"

    def __str__(self) -> str:
        return f"{self.year}-{self.month:02}"

    @staticmethod
    def get_period_from_date(payment_date):
        try:
            return Period.objects.get(year=payment_date.year, month=payment_date.month)
        except Period.DoesNotExist:
            return None


class Currency(models.Model):
    name = models.CharField(max_length=100)
    alpha3 = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        verbose_name = "Moneda"
        verbose_name_plural = "Monedas"

    def __str__(self) -> str:
        return self.name


class CurrencyConvert(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    exchange = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Conversion de moneda"
        verbose_name_plural = "Conversiones de monedas"

    def __str__(self) -> str:
        return f"{self.date} > {self.currency}"


class Account(models.Model):
    DEBE = -1
    HABER = 1
    SIGN_TYPE = (
        (DEBE, "Debe (-)"),
        (HABER, "Haber (+)"),
    )
    FIXED = "FIX"
    VARIABLE = "VAR"
    ACCOUNT_TYPE = (
        (FIXED, "Fijo"),
        (VARIABLE, "Variable"),
    )
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    sign = models.IntegerField(choices=SIGN_TYPE)
    account_type = models.CharField(
        max_length=5, choices=ACCOUNT_TYPE, default=VARIABLE
    )

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self) -> str:
        _sign = "-" if self.sign == -1 else "+"
        p_name = f" < {self.parent.name}" if self.parent else ""
        return f"{_sign}{self.name} {p_name} [{self.account_type}]"

class Accountable(CreationModificationDateMixin):
    period = models.ForeignKey(Period, on_delete=models.DO_NOTHING)
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=13, decimal_places=2)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.period} => {self.account}: {self.currency.alpha3} {self.amount}"

    @property
    def amount_str(self):
        return f"{self.currency.alpha3} {self.amount}"

    @property
    def get_signed_value(self) -> float:
        return self.amount * self.account.sign


def expense_upload_path(instance, filename):
    now = timezone.now()
    return f"expenses/{now.strftime('%Y/%m')}/{filename}"


class Upload(CreationModificationDateMixin):
    file = models.FileField(blank=True, null=True, upload_to=expense_upload_path)
    lines = models.IntegerField(default=0)
    result = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Subida de archivo"
        verbose_name_plural = "Subidas de archivos"

    def __str__(self) -> str:
        return str(self.file.name)


class Expense(Accountable):
    description = models.CharField(max_length=255, blank=True, null=True)
    payment_date = models.DateField(default=timezone.now, blank=True, null=True)
    local_amount = models.DecimalField(
        max_digits=13, decimal_places=2, default=0, editable=False
    )
    upload = models.ForeignKey(
        Upload,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"

    def __str__(self) -> str:
        return super().__str__()

    @property
    def get_local_amount(self) -> Decimal:
        data = (
            CurrencyConvert.objects.filter(
                currency=self.currency,
                date__lte=self.payment_date + timedelta(days=30),
                date__gte=self.payment_date - timedelta(days=30),
            )
            .annotate(date_difference=Abs(F("date") - self.payment_date))
            .order_by("date_difference")
            .values("exchange")[:1]
        )
        exchange = data[0]["exchange"] if data else 1
        return Decimal(self.amount) * Decimal(self.account.sign) * Decimal(exchange)

    def save(self, *args, **kwargs):
        self.local_amount = self.get_local_amount
        super(Expense, self).save(*args, **kwargs)


class AccountAsociation(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Asociacion de cuenta"
        verbose_name_plural = "Asociaciones de cuentas"

    def __str__(self) -> str:
        return f"{self.account.name} -> {self.token}"
