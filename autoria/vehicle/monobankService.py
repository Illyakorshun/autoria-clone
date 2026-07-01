import requests
from django.conf import settings
from vehicle.models import Payment


def create_monobank_invoice(payment: Payment, redirect_url: str, webhook_url: str, destination: str = None) -> str:

    headers = {
        'X-Token': settings.MONOBANK_TOKEN,
    }

    payload = {
        "amount": payment.amount,
        "ccy": 980,
        "merchantPaymInfo": {
            "reference": str(payment.reference),
            "destination": destination or "Оплата заказа на тестовом стенде",
        },
        "redirectUrl": redirect_url,
        "webHookUrl": webhook_url,
    }

    response = requests.post(settings.MONOBANK_INVOICE_URL, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json()

    payment.invoice_id = data.get('invoiceId')
    payment.save(update_fields=['invoice_id'])

    return data.get('pageUrl')


def get_monobank_invoice_status(payment: Payment) -> dict:
    if not payment.invoice_id:
        return {}

    headers = {
        'X-Token': settings.MONOBANK_TOKEN,
    }
    status_url = getattr(
        settings,
        'MONOBANK_INVOICE_STATUS_URL',
        'https://api.monobank.ua/api/merchant/invoice/status',
    )

    response = requests.get(status_url, params={'invoiceId': payment.invoice_id}, headers=headers)
    response.raise_for_status()
    return response.json()
