import omise
from typing import Optional
from django.conf import settings

from .... import TransactionKind
from ....interface import GatewayConfig, GatewayResponse, PaymentData, PaymentMethodInfo


OMISE_CREDIT_CARD = "omise_credit_card"

omise.api_secret = settings.OMISE_API_KEY


def validate_token(token: Optional[str]):
    #TODO: Check Omise Token Vidation
    return token

def create_charge(payment_information: PaymentData, capture=False, voided=False):
    #FIXME: not sure how it will be used.
    return_uri = ""
    charge_data = {
        "amount": int(payment_information.amount*100),
        "currency": payment_information.currency,
        "card": payment_information.token,
        "return_uri": return_uri
    }
    if voided:
        charge_data.update({"voided": voided})
    else:
        charge_data.update({"capture": capture})

    return omise.Charge.create(**charge_data)

def get_client_token(**_):
    #TODO: Get token from payment information
    return None


def authorize(
    payment_information: PaymentData, config: GatewayConfig
) -> GatewayResponse:
    error = validate_token(payment_information.token)
    success = not error
    if not success:
        error = f"Payment auth failed, invalid payment token."

    charge = create_charge(payment_information)

    transaction_kind = TransactionKind.AUTH
    if not charge.authorized:
        transaction_kind = TransactionKind.PENDING
        error = f"Payment auth failed, code: {charge.failure_code}, message: {charge.failure_message}"
        success = False

    action_required = not success

    card = charge.card

    return GatewayResponse(
        is_success=success,
        action_required=action_required,
        kind=transaction_kind,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=charge.transaction,
        error=error,
        payment_method_info=PaymentMethodInfo(
            last_4=card.last_digits,
            exp_year=card.expiration_year,
            exp_month=card.expiration_month,
            brand=card.brand,
            name=card.name,
            type=OMISE_CREDIT_CARD,
        ),
    )


def void(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    error = validate_token(payment_information.token)
    success = not error
    if not success:
        error = f"Payment void failed, invalid payment token."

    charge = create_charge(payment_information, voided=True)

    transaction_kind = TransactionKind.VOID
    if not charge.voided:
        transaction_kind = payment_information.kind
        error = f"Payment capture failed, code: {charge.failure_code}, message: {charge.failure_message}"
        success = False

    action_required = not success

    card = charge.card

    return GatewayResponse(
        is_success=success,
        action_required=action_required,
        kind=transaction_kind,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=charge.transaction,
        error=error,
        payment_method_info=PaymentMethodInfo(
            last_4=card.last_digits,
            exp_year=card.expiration_year,
            exp_month=card.expiration_month,
            brand=card.brand,
            name=card.name,
            type=OMISE_CREDIT_CARD,
        ),
    )


def capture(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    """Perform capture transaction."""
    error = validate_token(payment_information.token)
    success = not error
    if not success:
        error = f"Payment auth failed, invalid payment token."

    charge = create_charge(payment_information, capture=True)

    transaction_kind = TransactionKind.CAPTURE
    if not charge.authorized:
        transaction_kind = TransactionKind.CAPTURE_FAILED
        error = f"Payment capture failed, code: {charge.failure_code}, message: {charge.failure_message}"
        success = False

    action_required = not success

    card = charge.card

    return GatewayResponse(
        is_success=success,
        action_required=action_required,
        kind=transaction_kind,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=charge.transaction,
        error=error,
        payment_method_info=PaymentMethodInfo(
            last_4=card.last_digits,
            exp_year=card.expiration_year,
            exp_month=card.expiration_month,
            brand=card.brand,
            name=card.name,
            type=OMISE_CREDIT_CARD,
        ),
    )


def confirm(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    """Perform confirm transaction."""
    error = None
    success = dummy_success()
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
    error = None
    success = dummy_success()
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


def process_payment(
    payment_information: PaymentData, config: GatewayConfig
) -> GatewayResponse:
    """Process the payment."""
    token = payment_information.token
    authorize_response = authorize(payment_information, config)
    if not config.auto_capture:
        return authorize_response

    return capture(payment_information, config)
