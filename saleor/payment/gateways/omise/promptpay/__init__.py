import omise

from promptpay import qrcode

from django.conf import settings
from saleor.payment.models import Payment

from .... import ChargeStatus, TransactionKind
from ....interface import GatewayConfig, GatewayResponse, PaymentData, PaymentMethodInfo

from omise_payment.models import Payment as OmisePayment

omise.api_secret = settings.OMISE_API_KEY


def create_charge(config: GatewayConfig, payment_information: PaymentData):
    return omise.Charge.create(
        amount=int(payment_information.amount * 100),
        currency=payment_information.currency,
        source={ "type": "promptpay" }
    )

def authorize(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    """Perform capture transaction. Will be done manually via dashboard"""
    """TODO: Store payment transfer prove"""
    error = None
    success = True
    if not success:
        error = "Unable to process capture"

    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.AUTH,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=payment_information.token or "",
        error=error
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
    if not OmisePayment.objects.filter(payment_id=payment_information.payment_id):
        payment = Payment.objects.get(id=payment_information.payment_id)
        charge = create_charge(config, payment_information)
        #TODO: order is not present, at this state
        OmisePayment.objects.create(
            order = payment.order,
            payment=payment,
            source_id=charge.source.id,
            source_type=charge.source.type,
            charge_id=charge.id,
            amount=charge.amount,
            amount_net=charge.net,
            amount_fee=charge.fee,
            currency=charge.currency,
            qr_code_url=charge.source.scannable_code.image.download_uri
        )

    action_required_data = {
        "qr_code_url": charge.source.scannable_code.image.download_uri
    }

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

    return pending(payment_information, config)
