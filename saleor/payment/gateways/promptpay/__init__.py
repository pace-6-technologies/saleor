import uuid

from promptpay import qrcode

from saleor.payment.models import Payment

from ... import ChargeStatus, TransactionKind
from ...interface import GatewayConfig, GatewayResponse, PaymentData, PaymentMethodInfo

from p6promptpay.models import PromptPayPayment


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
    promptpay_id=config.connection_params['promptpay_id']
    amount = payment_information.amount

    if not PromptPayPayment.objects.filter(payment_id=payment_information.payment_id):
        payment = Payment.objects.get(id=payment_information.payment_id)
        qr_code = qrcode.generate_payload(promptpay_id, amount)
        #TODO: order is not present, at this state
        PromptPayPayment.objects.create(
            order = payment.order,
            payment=payment,
            promptpay_id=promptpay_id,
            amount=amount,
            qr_code=qr_code
        )

    action_required_data = {"qr_code": qr_code}

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
            name="PromptPay",
            type="promptpay",
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
