from typing import TYPE_CHECKING

from saleor.plugins.base_plugin import BasePlugin, ConfigurationTypeField

from ..utils import get_supported_currencies, require_active_plugin
from . import (
    GatewayConfig,
    capture,
    confirm,
    process_payment,
    refund,
    void,
)

from promptpay import qrcode

GATEWAY_NAME = "PromptPay"

if TYPE_CHECKING:
    from ...interface import GatewayResponse, PaymentData, TokenConfig


class PromptPayGatewayPlugin(BasePlugin):
    PLUGIN_ID = "pace6.payments.promptpay"
    PLUGIN_NAME = GATEWAY_NAME
    DEFAULT_ACTIVE = False
    DEFAULT_CONFIGURATION = [
        {"name": "PromptPay ID", "value": ""},
        {"name": "Supported currencies", "value": "THB"},
    ]
    CONFIG_STRUCTURE = {
        "PromptPay ID": {
            "type": ConfigurationTypeField.STRING,
            "help_text": "PromptPay Id, can be mobilephone or citizen id.",
            "label": "PromptPay ID",
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
                'promptpay_id': configuration["PromptPay ID"]
            },
        )
        self.promptpay_id = configuration["PromptPay ID"]

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
            { "field": "promptpay_id", "value": "xxxxxxxxxx"}
        ]
