from products import Product
from typing import List, Tuple


class Store:
    """Manages a collection of products in a store."""

    def __init__(self, products: List[Product]):
        self.products = products  # List of products in the store

    def add_product(self, product: Product):
        """Adds a product to the store."""
        self.products.append(product)

    def remove_product(self, product: Product):
        """Removes a product from the store."""
        if product in self.products:
            self.products.remove(product)
        else:
            raise ValueError(f"Product {product.name} not found in the store.")

    def get_total_quantity(self) -> int:
        """Returns total quantity of all active products."""
        return sum(p.get_quantity() for p in self.products if p.is_active())

    def get_all_products(self) -> List[Product]:
        """Returns a list of all active products."""
        return [p for p in self.products if p.is_active()]

    def order(self, shopping_list: List[Tuple[Product, int]]) -> float:
        """Processes an order and returns total price."""
        total_price = 0
        for product, quantity in shopping_list:
            if product.is_active() and product.get_quantity() >= quantity:
                total_price += product.buy(quantity)  # Purchase and get the price
            else:
                raise ValueError(
                    f"Cannot purchase {quantity} of {product.name}. Not enough quantity or inactive product.")
        return total_price
