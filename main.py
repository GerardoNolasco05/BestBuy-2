from products import Product, NonStockedProduct, LimitedProduct, SecondHalfPrice, ThirdOneFree, PercentDiscount
from store import Store


def list_all_products(store: Store):
    """Lists all active products in the store with a numbered format."""
    active_products = store.get_all_products()
    if active_products:
        print("------")
        for i, product in enumerate(active_products, start=1):
            print(f"{i}. {product.show()}")
        print("------")
    else:
        print("No active products in the store.")

def show_total_quantity(store: Store):
    """Shows the total quantity of all active products in the store."""
    total_quantity = store.get_total_quantity()
    print(f"Total of {total_quantity} items in store")

def make_order(store: Store):
    """Allows the user to make an order."""
    shopping_list = []
    list_all_products(store)
    print("When you want to finish order, enter empty text.")
    while True:
        product_choice = input("Which product # do you want? ")
        if product_choice == "":
            break
        quantity_choice = input("What amount do you want? ")
        if quantity_choice == "":
            break
        try:
            product_index = int(product_choice) - 1
            quantity = int(quantity_choice)
            active_products = store.get_all_products()
            if 0 <= product_index < len(active_products):
                selected_product = active_products[product_index]
                if 1 <= quantity <= selected_product.get_quantity():
                    shopping_list.append((selected_product, quantity))
                    print("Product added to list!")
                else:
                    print("Error adding product!")
            else:
                print("Error adding product!")
        except ValueError:
            print("Error adding product!")
    if shopping_list:
        try:
            total_cost = store.order(shopping_list)
            print(f"Order total cost: {total_cost} dollars.")
        except ValueError as e:
            print(e)
    else:
        print("No items added to the order.")

def start(store: Store):
    """Shows the user interface menu and allows interaction."""
    while True:
        print("\n    Store Menu")
        print("    ----------")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")
        choice = input("Please choose a number: ")
        if choice == '1':
            list_all_products(store)
        elif choice == '2':
            show_total_quantity(store)
        elif choice == '3':
            make_order(store)
        elif choice == '4':
            break


def main():
    """Sets up the store with initial inventory and starts the user interface."""
    # Setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]

    # Create promotion catalog
    second_half_price = SecondHalfPrice("Second Half Price!")
    third_one_free = ThirdOneFree("Third One Free!")
    thirty_percent = PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)  # MacBook Air M2
    product_list[1].set_promotion(third_one_free)  # Bose QuietComfort Earbuds
    product_list[3].set_promotion(thirty_percent)  # Windows License

    # Create the store and start the program
    best_buy = Store(product_list)
    start(best_buy)

if __name__ == "__main__":
    main()
