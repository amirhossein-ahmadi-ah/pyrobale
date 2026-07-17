from typing import Optional

class SuccessfulPayment:
    def __init__(
        self,
        currency: Optional[str],
        total_amount: Optional[int],
        invoice_payload: Optional[str],
        telegram_payment_charge_id: Optional[str],
        provider_payment_charge_id: Optional[str],
        **kwargs
    ):
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id
        for key, value in kwargs.items():
            setattr(self, key, value)
