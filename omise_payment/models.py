from decimal import Decimal

from django.db import models
from django.conf import settings

from saleor.payment.models import Payment
from saleor.order.models import Order

class PromptPayPayment(models.Model):
    payment = models.OneToOneField(
        Payment,
        related_name="omise_promptpay_payments", on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, null=True, related_name="omise_promptpay_payments", on_delete=models.PROTECT
    )
    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    amount_net = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    amount_fee = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    currency = models.CharField(max_length=5)
    charge_id = models.CharField(max_length=200)
    source_id = models.CharField(max_length=200)
    qr_code_url = models.TextField(max_length=1000)
    
    def __str__(self):
        return "PromptPayPayment(Order: {}, promtpay id: {}, amount: {})".format(self.promptpay_id, self.amount)