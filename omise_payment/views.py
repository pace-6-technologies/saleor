import copy, json, datetime
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from saleor.payment import PaymentError, gateway
from saleor.payment.models import Payment
from .models import Webhook, Payment as OmisePayment

def get_payment(data: dict):
    charge_id = data['id']
    source_id = data['source']['id']
    source_type = data['source']['type']
    omise_payments = OmisePayment.objects.filter(
        charge_id=charge_id,
        source_id=source_id,
        source_type=source_type
    )

    if not omise_payments:
        raise Http404("Payment not found, ")

    return Payment.objects.get(id=omise_payments[0].payment_id)

@csrf_exempt
@require_POST
def webhook(request):
    jsondata = request.body
    data = json.loads(jsondata)
    meta = {}
    for k, v in request.headers.items():
        if isinstance(v, str):
            meta[k] = v

    event_key = data['key']

    Webhook.objects.create(  
        event=data['id'],
        key=event_key,
        event_timestamp=data['created_at'],
        request_data=data,
        request_header_data=meta      
    )

    if event_key in ['charge.capture']:
        pass
    if event_key in ['charge.complete']:
        payment = get_payment(data['data'])
        gateway.authorize(payment, payment.token)
        gateway.capture(payment)
        pass
    if event_key in ['charge.create']:
        pass
    if event_key in ['charge.expire']:
        #TODO: cancel the order?
        pass
    if event_key in ['charge.reverse']:
        pass
    if event_key in ['charge.update']:
        pass
    return HttpResponse(status=200)