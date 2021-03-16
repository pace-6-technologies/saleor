from decimal import Decimal

OMISE_PUBLIC_KEY_CONFIG_NAME = "Omise Public Key"
OMISE_PUBLIC_KEY_CONFIG_TXT = "Omise API Public Key"
OMISE_PUBLIC_KEY = "api_public_key"

def get_amount_for_omise(amount):
    return int(amount*100)


def get_amount_from_omise(amount):
    amount = Decimal(amount)
    amount /= Decimal(100)
    return amount