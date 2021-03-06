import uuid

from promptpay import qrcode

from django.conf import settings
from saleor.payment.models import Payment

from .... import ChargeStatus, TransactionKind
from ....interface import GatewayConfig, GatewayResponse, PaymentData, PaymentMethodInfo

from omise_payment.models import PromptPayPayment

 omise.api_secret = settings.OMISE_API_KEY

 
def create_charge(amount, currency="THB"):
    return omise.Charge.create(
        amount = int(amount * 100),
        currency="THB",
        source = { "type": "promptpay" }
    )

def capture(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    """Perform capture transaction. Will be done manually via dashboard"""
    """TODO: Store payment transfer prove"""
    error = None
    success = True
    if not success:
        error = "Unable to process capture"

    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.CAPTURE,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=payment_information.token or "",
        error=error
    )


def confirm(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    """Perform confirm transaction."""
    error = None
    success = True
    if not success:
        error = "Unable to process capture"

    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.CAPTURE,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=payment_information.token or "",
        error=error,
    )


def refund(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    """Perform refund transaction. Will be done manually via dashboard"""
    error = None
    success = True
    if not success:
        error = "Unable to process refund"
    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.REFUND,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=payment_information.token or "",
        error=error,
    )

def void(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    """Perform void transaction. Will be done manually via dashboard"""
    error = None
    success = True
    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.VOID,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=payment_information.token or "",
        error=error,
    )

def pending(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    error = None
    success = True
    amount = payment_information.amount

    if not PromptPayPayment.objects.filter(payment_id=payment_information.payment_id):
        payment = Payment.objects.get(id=payment_information.payment_id)
        amount = payment_information.amount
        charge = create_charge(config, amount)

        #TODO: order is not present, at this state
        PromptPayPayment.objects.create(
            order = payment.order,
            payment=payment,
            source_id=charge_id.source.id,
            charge_id=charge.id,
            amount=charge.amount,
            amount_net=charge.net,
            amount_fee=charge.fee,
            currency=charge.currency,
            qr_code_url=charge.source.scannable_code.image.download_url
        )

    action_required_data = {"qr_code_url": charge.source.scannable_code.image.download_url}

    return GatewayResponse(
        is_success=success,
        action_required=True,
        action_required_data=action_required_data,
        kind=TransactionKind.PENDING,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=payment_information.token or "",
        error=error,
        payment_method_info=PaymentMethodInfo(
            name="Omise PromptPay",
            type="omise_promptpay",
        ),
    )

def process_payment(
    payment_information: PaymentData, config: GatewayConfig
) -> GatewayResponse:
    """Process the payment."""
    token = payment_information.token

    # Process payment normally if payment token is valid
    if token not in dict(ChargeStatus.CHOICES):
        return pending(payment_information, config)

    # Process payment by charge status which is selected in the payment form
    # Note that is for testing by dummy gateway only
    charge_status = token

    capture_response = capture(payment_information, config)
    if charge_status == ChargeStatus.FULLY_REFUNDED:
        return refund(payment_information, config)
    return capture_response
