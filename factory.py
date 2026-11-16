from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def validate(self, details: dict) -> bool:
        pass

    @abstractmethod
    def compute_fee(self, amount: float) -> float:
        pass

    @property
    @abstractmethod
    def method(self) -> str:
        pass

    def error_message(self) -> str:
        return f"Invalid {self.method} details"

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": self.error_message()}
        fee = round(self.compute_fee(amount), 2)
        return {"success": True, "method": self.method, "amount": round(amount + fee, 2), "fee": fee}


class CreditCardProcessor(PaymentProcessor):
    method = "credit_card"

    def validate(self, details: dict) -> bool:
        card_number = details.get("card_number")
        cvv = details.get("cvv")
        return bool(card_number) and len(card_number) == 16 and bool(cvv) and len(cvv) == 3

    def compute_fee(self, amount: float) -> float:
        return amount * 0.029


class BankTransferProcessor(PaymentProcessor):
    method = "bank_transfer"

    def validate(self, details: dict) -> bool:
        iban = details.get("iban")
        return bool(iban) and len(iban) >= 15

    def compute_fee(self, amount: float) -> float:
        return 1.50


class PayPalProcessor(PaymentProcessor):
    method = "paypal"

    def validate(self, details: dict) -> bool:
        email = details.get("email")
        return bool(email) and "@" in email

    def compute_fee(self, amount: float) -> float:
        return amount * 0.034 + 0.30


class PaymentFactory:
    _processors = {
        "credit_card": CreditCardProcessor,
        "bank_transfer": BankTransferProcessor,
        "paypal": PayPalProcessor,
    }

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        processor_class = self._processors.get(payment_type)
        if processor_class is None:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return processor_class()

    @classmethod
    def register(cls, payment_type: str, processor_class: type) -> None:
        cls._processors[payment_type] = processor_class


class ApplePayProcessor(PaymentProcessor):
    method = "apple_pay"

    def validate(self, details: dict) -> bool:
        return bool(details.get("token"))

    def compute_fee(self, amount: float) -> float:
        return amount * 0.015


if __name__ == "__main__":
    factory = PaymentFactory()

    processor = factory.get_processor("credit_card")
    print(processor.process(100.0, {"card_number": "1234567890123456", "cvv": "123"}))

    processor = factory.get_processor("bank_transfer")
    print(processor.process(100.0, {"iban": "FR7630006000011234567890189", "bic": "BNPAFRPP"}))

    processor = factory.get_processor("paypal")
    print(processor.process(100.0, {"email": "client@mail.com"}))

    print(factory.get_processor("paypal").process(100.0, {"email": "wrong-email"}))

    PaymentFactory.register("apple_pay", ApplePayProcessor)
    print(factory.get_processor("apple_pay").process(100.0, {"token": "abc123"}))
