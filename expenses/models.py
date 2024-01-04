from decimal import Decimal
from datetime import timedelta
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

    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"

    def __str__(self) -> str:
        return f"{self.year}-{self.month:02}"


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
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    sign = models.IntegerField(choices=SIGN_TYPE)

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self) -> str:
        _sign = "-" if self.sign == -1 else "+"
        if not self.parent:
            return f"{self.name} [{_sign}]"
        else:
            return f"{self.name} ({self.parent.name}) [{_sign}]"


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


class Expense(Accountable):
    description = models.CharField(max_length=255, blank=True, null=True)
    payment_date = models.DateField(default=timezone.now, blank=True, null=True)
    local_amount = models.DecimalField(max_digits=13, decimal_places=2, default=0)

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


class Bank(models.Model):
    name = models.CharField(max_length=100)

class BankAccount(models.Model):
    code = models.CharField(max_length=50)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
