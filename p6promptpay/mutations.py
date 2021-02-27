import graphene
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from saleor.core.permissions import PaymentPermissions
from saleor.payment.error_codes import PaymentErrorCode
from saleor.graphql.core.mutations import BaseMutation
from saleor.graphql.core.types.common import PaymentError

from p6promptpay.models import PromptPayPayment
from p6promptpay.types import PromptPayPaymentType


class PromptPayPaymentUpdateInput(graphene.InputObjectType):
    payment_proof_image_base64 = graphene.String(required=True)
    payment_proof_image_file_name = graphene.String(required=True)
    payment_proof_upload_note = graphene.String(required=True)
    payment_proof_upload_note_order_id = graphene.String(required=True)
    payment_proof_upload_timestamp = graphene.String(required=True)


class PromptPayPaymentUpdate(BaseMutation):
    promptpay_payment = graphene.Field(PromptPayPaymentType)

    class Arguments:
        token = graphene.String(required=True, description="Token of the promptpay payment to update.")
        input = PromptPayPaymentUpdateInput(
            description="Fields required.",
            required=True,
        )

    class Meta:
        description = "Update promptpay payment."
        #permissions = (PaymentPermissions.MANAGE_PAYMENTS,)
        error_type_class = PaymentError
        error_type_field = "payments_errors"

    @classmethod
    def perform_mutation(cls, root, info, **data):
        token = data.get("token")
        data = data.get("input")
        #TODO: validation
        promptpay_payments = PromptPayPayment.objects.filter(payment__token=token)
        if not promptpay_payments:
            raise ObjectDoesNotExist(f"Payment with token: {token} does not exist.")

        promptpay_payments.update(**data)

        return PromptPayPaymentUpdate(
            promptpay_payment=PromptPayPayment.objects.get(payment__token=token))
