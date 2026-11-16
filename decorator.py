from abc import ABC, abstractmethod


class OrderComponent(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


class BaseOrder(OrderComponent):
    def __init__(self, base_price: float):
        self.base_price = base_price

    def get_cost(self) -> float:
        return self.base_price

    def get_description(self) -> str:
        return f"Base price: {self.base_price:.2f}€"


class OrderDecorator(OrderComponent):
    def __init__(self, order: OrderComponent):
        self._order = order

    def get_cost(self) -> float:
        return self._order.get_cost()

    def get_description(self) -> str:
        return self._order.get_description()


class ExpressShippingDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self._order.get_cost() + 15.00

    def get_description(self) -> str:
        return self._order.get_description() + "\nExpress shipping: +15.00€"


class InsuranceDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self._order.get_cost() * 1.05

    def get_description(self) -> str:
        insurance = self._order.get_cost() * 0.05
        return self._order.get_description() + f"\nInsurance (5%): +{insurance:.2f}€"


class GiftWrapDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self._order.get_cost() + 5.00

    def get_description(self) -> str:
        return self._order.get_description() + "\nGift wrap: +5.00€"


class DiscountDecorator(OrderDecorator):
    def __init__(self, order: OrderComponent, percent: float):
        super().__init__(order)
        self.percent = percent

    def get_cost(self) -> float:
        return self._order.get_cost() * (1 - self.percent / 100)

    def get_description(self) -> str:
        discount = self._order.get_cost() * self.percent / 100
        return self._order.get_description() + f"\nDiscount ({self.percent}%): -{discount:.2f}€"


class PremiumMemberDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self._order.get_cost() * 0.90

    def get_description(self) -> str:
        discount = self._order.get_cost() * 0.10
        return self._order.get_description() + f"\nPremium member (10%): -{discount:.2f}€"


if __name__ == "__main__":
    simple = BaseOrder(100.00)
    print(simple.get_description())
    print(f"Total: {simple.get_cost():.2f}€")

    print("\n---\n")

    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)

    print(order.get_description())
    print(f"Total: {order.get_cost():.2f}€")
