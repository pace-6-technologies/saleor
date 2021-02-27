import graphene
from graphene import relay, ObjectType

from graphene_django import DjangoObjectType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from saleor.order.models import Order
from saleor.payment.models import Payment

from saleor.graphql.order.types import Order

from p6promptpay.models import PromptPayPayment

class PromptPayPaymentType(DjangoObjectType):
    class Meta:
        model = PromptPayPayment
        fields = (
            "payment",
            "qr_code",
            "payment_proof_image_base64", 
            "payment_proof_image_file_name",
            "payment_proof_upload_note", 
            "payment_proof_upload_note_order_id", 
            "payment_proof_upload_timestamp"
        )
        filter_fields = ["payment", "order"]
        interfaces = (relay.Node, )
