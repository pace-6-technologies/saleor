from decimal import Decimal

from django.db import models
from django.conf import settings

from saleor.payment.models import Payment
from saleor.order.models import Order

class PromptPayPayment(models.Model):
    payment = models.OneToOneField(
        Payment, 
        related_name="promptpay_payments", on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, null=True, related_name="promptpay_payments", on_delete=models.PROTECT
    )
    promptpay_id = models.CharField(max_length=13)
    qr_code = models.CharField(max_length=1000)
    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )

    def __str__(self):
        return "PromptPayPayment(Order: {}, promtpay id: {}, amount: {})".format(self.promptpay_id, self.amount)