from abc import ABC, abstractmethod


class Product:
    """
    A class representing a product with a name, price, and quantity.
    """

    def __init__(self, name: str, price: float, quantity: int):
        if not name or price < 0 or quantity < 0:
            raise ValueError("Invalid input: Name cannot be empty, price and quantity must be non-negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True  # Product is active by default
        self.promotion = None  # Store promotion, if applicable

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def set_promotion(self, promotion):
        """Assign a promotion to the product."""
        self.promotion = promotion

    def get_promotion(self):
        """Returns the current promotion, if any."""
        return self.promotion

    def show(self) -> str:
        """Display product details, including promotions if applicable."""
        promo_text = f" | Promotion: {self.promotion}" if self.promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}{promo_text}"

    def buy(self, quantity: int) -> float:
        """
        Processes the purchase of a given quantity of the product.
        Applies promotions if available.
        """
        if not self.active:
            raise Exception(f"The product '{self.name}' is no longer available.")

        if quantity <= 0:
            raise ValueError("Quantity to buy must be greater than 0.")

        if quantity > self.quantity:
            raise ValueError("Not enough quantity available.")

        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity

        self.set_quantity(self.quantity - quantity)  # Update quantity
        return total_price


class NonStockedProduct(Product):
    """
    A product that doesn't have a quantity to track (e.g., software licenses).
    """

    def __init__(self, name: str, price: float):
        super().__init__(name, price, 0)

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, (Non-stocked, no quantity)"

    def buy(self, quantity: int) -> float:
        if quantity != 1:
            raise ValueError("Non-stocked products can only be bought in quantities of 1.")
        return self.price


class LimitedProduct(Product):
    """
    A product that can only be purchased a limited number of times in one order.
    """

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Max per order: {self.maximum}"

    def buy(self, quantity: int) -> float:
        if quantity > self.maximum:
            raise ValueError(f"Only {self.maximum} of this product can be purchased per order.")

        return super().buy(quantity)


class Promotion(ABC):
    """
    Abstract class for promotions.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """
        Apply promotion logic to calculate discounted price.
        """
        pass

    def __str__(self):
        return self.name


class PercentDiscount(Promotion):
    """
    Applies a percentage discount on the product price.
    """
    def __init__(self, name: str, percent: float):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        discount_price = product.price * (1 - self.percent / 100)
        return discount_price * quantity


class SecondHalfPrice(Promotion):
    """
    Second item is at half price.
    """
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        full_price_items = quantity // 2 + quantity % 2
        half_price_items = quantity // 2
        return full_price_items * product.price + half_price_items * (product.price * 0.5)


class ThirdOneFree(Promotion):
    """
    Buy 2, get 1 free.
    """
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        paid_items = quantity - (quantity // 3)
        return paid_items * product.price
