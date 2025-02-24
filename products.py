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
        self.active = True  # Product is active by default when created

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

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity: int) -> float:
        """
        Processes the purchase of a given quantity of the product.
        """
        if not self.active:
            raise Exception(f"The product '{self.name}' is no longer available.")

        if quantity <= 0:
            raise ValueError("Quantity to buy must be greater than 0.")

        if quantity > self.quantity:
            raise ValueError("Not enough quantity available.")

        total_price = self.price * quantity
        self.set_quantity(self.quantity - quantity)  # Update quantity
        return total_price


class NonStockedProduct(Product):
    """
    A product that doesn't have a quantity to track.
    Example: Microsoft Windows License.
    """

    def __init__(self, name: str, price: float):
        # Quantity is set to 0 and will always remain 0
        super().__init__(name, price, 0)

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, (Non-stocked, no quantity)"

    def buy(self, quantity: int) -> float:
        # No need to check quantity since it's non-stocked
        if quantity != 1:
            raise ValueError("Non-stocked products can only be bought in quantities of 1.")
        return self.price  # No quantity to decrease, just charge the price


class LimitedProduct(Product):
    """
    A product that can only be purchased a limited number of times in one order.
    Example: Shipping fee.
    """

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        # Maximum is an additional parameter
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Maximum purchase per order: {self.maximum}"

    def buy(self, quantity: int) -> float:
        # Ensure quantity does not exceed the maximum allowed
        if quantity > self.maximum:
            raise ValueError(f"Error while making order! Only {self.maximum} is allowed from this product!.")

        # Continue with regular product purchase logic
        if quantity > self.quantity:
            raise ValueError("Not enough quantity available.")

        total_price = self.price * quantity
        self.set_quantity(self.quantity - quantity)  # Update quantity
        return total_price
