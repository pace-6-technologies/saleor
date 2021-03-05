from typing import TYPE_CHECKING

import omise

from saleor.plugins.base_plugin import BasePlugin, ConfigurationTypeField

from ...utils import get_supported_currencies, require_active_plugin

from ....interface import GatewayConfig

from ..promptpay import capture, confirm, refund, pending, void, process_payment
from ...omise import OMISE_PUBLIC_KEY, OMISE_PUBLIC_KEY_CONFIG_NAME, OMISE_PUBLIC_KEY_CONFIG_TXT

GATEWAY_NAME = "Omise PromptPay"

if TYPE_CHECKING:
    from ...interface import GatewayResponse, PaymentData, TokenConfig


class OmisePromptPayGatewayPlugin(BasePlugin):
    PLUGIN_ID = "pace6.payments.omise.promptpay"
    PLUGIN_NAME = GATEWAY_NAME
    DEFAULT_ACTIVE = False
    DEFAULT_CONFIGURATION = [
        {"name": OMISE_PUBLIC_KEY_CONFIG_NAME, "value": ""},
        {"name": "Supported currencies", "value": "THB"},
    ]
    CONFIG_STRUCTURE = {
        OMISE_PUBLIC_KEY_CONFIG_NAME: {
            "type": ConfigurationTypeField.STRING,
            "help_text": OMISE_PUBLIC_KEY_CONFIG_TXT,
            "label": OMISE_PUBLIC_KEY_CONFIG_TXT,
        },
        "Supported currencies": {
            "type": ConfigurationTypeField.STRING,
            "help_text": "Determines currencies supported by gateway."
            " Please enter currency codes separated by a comma.",
            "label": "Supported currencies",
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        configuration = {item["name"]: item["value"] for item in self.configuration}
        self.config = GatewayConfig(
            gateway_name=GATEWAY_NAME,
            auto_capture=False,
            supported_currencies=configuration["Supported currencies"],
            connection_params = {
                OMISE_PUBLIC_KEY: configuration[OMISE_PUBLIC_KEY_CONFIG_NAME]
            },
        )

    def _get_gateway_config(self):
        return self.config

    @require_active_plugin
    def authorize_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return authorize(payment_information, self._get_gateway_config())

    @require_active_plugin
    def capture_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return capture(payment_information, self._get_gateway_config())

    @require_active_plugin
    def confirm_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return confirm(payment_information, self._get_gateway_config())

    @require_active_plugin
    def refund_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return refund(payment_information, self._get_gateway_config())

    @require_active_plugin
    def void_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return void(payment_information, self._get_gateway_config())

    @require_active_plugin
    def process_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return process_payment(payment_information, self._get_gateway_config())

    @require_active_plugin
    def get_supported_currencies(self, previous_value):
        config = self._get_gateway_config()
        return get_supported_currencies(config, GATEWAY_NAME)

    @require_active_plugin
    def get_payment_config(self, previous_value):
        config = self._get_gateway_config()
        return [
            { "field": OMISE_PUBLIC_KEY, "value": config.connection_params[OMISE_PUBLIC_KEY]}
        ]
