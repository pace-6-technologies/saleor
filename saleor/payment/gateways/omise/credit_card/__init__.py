import omise
from typing import Optional
from django.conf import settings

from .... import TransactionKind
from ....interface import GatewayConfig, GatewayResponse, PaymentData, PaymentMethodInfo
from ....models import Payment

from ...omise import OMISE_PUBLIC_KEY, get_amount_for_omise, get_amount_from_omise


OMISE_CREDIT_CARD = "omise_credit_card"

omise.api_secret = settings.OMISE_API_KEY


def validate_token(token: Optional[str]):
    #TODO: Check Omise Token Vidation
    return True

def create_charge(payment_information: PaymentData, capture=False, voided=False):
    #FIXME: not sure how it will be used.
    return_uri = ""
    charge_data = {
        "amount": get_amount_for_omise(payment_information.amount),
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

def get_cc_card_from_payment_token(token):
    payment = Payment.objects.get(token=payment_information.token)
    return omise.Base.from_data({
        "last_4": payment.cc_last_digits,
        "exp_year": payment.cc_exp_year,
        "exp_month": payment.cc_exp_month,
        "brand": payment.cc_brand
    })


def _error_response(
    kind: str,  # use TransactionKind class
    exc: omise.errors.BaseError,
    payment_info: PaymentData,
    charge: None,
    action_required: bool = False,
) -> GatewayResponse:
    currency = charge.currency if charge else currency
    amount = get_amount_from_omise(charge.amount) if charge else amount
    raw_response = charge.__dict__['_attributes'] if charge else {}
    return GatewayResponse(
        is_success=False,
        action_required=action_required,
        transaction_id=payment_info.token or "",
        amount=amount,
        currency=currency,
        error=f"{exc}",
        kind=kind,
        raw_response=raw_response
    )


def _success_response(
    charge: omise.Charge,
    kind: TransactionKind,
    success: bool = True,
    amount=None,
    currency=None,
    raw_response=None,
):
    currency = charge.currency if charge else currency
    amount = get_amount_from_omise(charge.amount) if charge else amount
    raw_response = charge.__dict__['_attributes'] if charge else {}
    return GatewayResponse(
        is_success=success,
        action_required=False,
        transaction_id=charge.id,
        amount=amount,
        currency=currency,
        error=None,
        kind=kind,
        raw_response=raw_response
    )

def fill_card_details(payment_token, response: GatewayResponse, omise_card=None):
    card = omise_card if omise_card else get_cc_card_from_payment_token(payment_token)
    payment_method_info = PaymentMethodInfo(
        last_4=card.last_digits,
        exp_year=card.expiration_year,
        exp_month=card.expiration_month,
        brand=card.brand,
        type=OMISE_CREDIT_CARD,
    )
    if card.name:
        payment_method_info.name = card.name
    response.payment_method_info = payment_method_info
    return response


def authorize(
    payment_information: PaymentData, config: GatewayConfig
) -> GatewayResponse:
    """Perform auth transaction."""
    """OMISE AUTO AUTH on OMISE.JS"""
    """NO OMISE AUTH CALL HERE"""
    token_valid = validate_token(payment_information.token)
    success = True
    card = None
    if token_valid:
        transaction_kind = TransactionKind.AUTH
        success = True      
    else:
        transaction_kind = TransactionKind.PENDING
        error = f"Payment auth failed, invalid payment token."

    response = _success_response(None, kind, success=success)
    return fill_card_details(payment_information.token, response, omise_card=None)


def void(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    token_valid = validate_token(payment_information.token)
    success = False
    card = None
    if token_valid:
        charge = create_charge(payment_information, void=True)
        transaction_kind = TransactionKind.VOID
        success = True
        card = charge.card
        if not charge.void:
            transaction_kind = TransactionKind.PENDING
            success = False
            error = f"Payment void failed, code: {charge.failure_code}, message: {charge.failure_message}"        
    else:
        transaction_kind = TransactionKind.PENDING
        error = f"Payment void failed, invalid payment token."

    response = _success_response(charge, kind, success=success)
    return fill_card_details(payment_information.token, response, omise_card=charge.card)


def capture(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    """Perform capture transaction."""
    token_valid = validate_token(payment_information.token)
    success = False
    card = None
    if token_valid:
        charge = create_charge(payment_information, capture=True)
        transaction_kind = TransactionKind.CAPTURE
        success = True
        card = charge.card
        if not charge.authorized:
            transaction_kind = TransactionKind.CAPTURE_FAILED
            success = False
            error = f"Payment capture failed, code: {charge.failure_code}, message: {charge.failure_message}"        
    else:
        transaction_kind = TransactionKind.CAPTURE_FAILED
        error = f"Payment capture failed, invalid payment token."

    response = _success_response(charge, transaction_kind, success=success)
    return fill_card_details(payment_information.token, response, omise_card=charge.card)


def process_payment(
    payment_information: PaymentData, config: GatewayConfig
) -> GatewayResponse:
    """Process the payment. Omise auto capture the money from omise.js"""
    token = payment_information.token
    if config.auto_capture:
         return capture(payment_information, config)
    return authorize(payment_information, config)

   
