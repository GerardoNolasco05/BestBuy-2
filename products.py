class Product:
    """
    A class representing a product with a name, price, and quantity.

    Attributes:
        name (str): The name of the product.
        price (float): The price per unit of the product.
        quantity (int): The available quantity of the product.
        active (bool): Indicates if the product is available for purchase.
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

        Args:
            quantity (int): The amount of the product to buy.

        Returns:
            float: The total price of the purchase.

        Raises:
            Exception: If the product is inactive.
            ValueError: If the quantity is non-positive or exceeds available stock.
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
