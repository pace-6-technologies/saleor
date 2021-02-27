import graphene

from graphene import relay, ObjectType

from graphene_django import DjangoObjectType
from graphene_django.types import DjangoObjectType, ObjectType
from graphene_django.filter import DjangoFilterConnectionField

from saleor.core.permissions import PaymentPermissions

from  saleor.graphql.core.fields import BaseDjangoConnectionField
from  saleor.graphql.decorators import permission_required

from saleor.payment.models import Payment

from p6promptpay.models import PromptPayPayment
from p6promptpay.types import PromptPayPaymentType
from p6promptpay.mutations import PromptPayPaymentUpdate, PromptPayPaymentUpdate


class PromptPayPaymentQueries(ObjectType):
    promptpay_payment_by_payment_token = graphene.Field(PromptPayPaymentType, payment_token=graphene.String())
    promptpay_payment_by_order_token = graphene.Field(PromptPayPaymentType, order_token=graphene.String())

    def resolve_promptpay_payment_by_payment_token(self, info, payment_token):
        payment = Payment.objects.get(token=payment_token)
        if payment:
            return PromptPayPayment.objects.get(payment_id=payment.id)

    def resolve_promptpay_payment_by_order_token(self, info, order_token):
        payment = Payment.objects.get(order__token=order_token)
        if payment:
            return PromptPayPayment.objects.get(payment_id=payment.id)


class PromptPayMutations(graphene.ObjectType):
    promtpay_payment_update = PromptPayPaymentUpdate.Field()

