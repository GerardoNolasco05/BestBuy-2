import pytest
from products import Product

def test_create_product():
    # Test that creating a normal product works
    product = Product(name="Test Product", price=100.0, quantity=10)

    # Assertions to check if the product is created correctly
    assert product.name == "Test Product"
    assert product.price == 100.0
    assert product.quantity == 10
    assert product.is_active() is True

def test_invalid_details():
    # Test for empty name
    with pytest.raises(ValueError, match="Invalid input: Name cannot be empty, price and quantity must be non-negative."):
        Product(name="", price=100.0, quantity=10)

    # Test for negative price
    with pytest.raises(ValueError, match="Invalid input: Name cannot be empty, price and quantity must be non-negative."):
        Product(name="Test Product", price=-50.0, quantity=10)


def test_product_inactive_zero():
    # Test that a product becomes inactive when its quantity reaches 0
    product = Product(name="Test Product", price=100.0, quantity=5)

    # Purchase some quantity and reduce it to 0
    product.buy(5)

    # Check if the product is inactive when quantity reaches 0
    assert product.get_quantity() == 0
    assert product.is_active() is False


def test_modifies_product_quantity_():
    # Test that product purchase modifies the quantity and returns the correct total price
    product = Product(name="Test Product", price=50.0, quantity=10)

    # Purchase 3 units of the product
    total_price = product.buy(3)

    # Assertions to check if the quantity is modified and total price is correct
    assert product.get_quantity() == 7  # 10 - 3 units purchased
    assert total_price == 150.0  # 3 * 50.0 = 150.0

def test_buying_larger_quantity_than_inventory():
    # Test that buying a larger quantity than exists invokes an exception
    product = Product(name="Test Product", price=50.0, quantity=5)

    # Try to buy more than available (e.g., 10 units when only 5 are available)
    with pytest.raises(ValueError, match="Not enough quantity available."):
        product.buy(10)

