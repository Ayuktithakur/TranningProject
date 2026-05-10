from abc import ABC, abstractmethod

class Product:
    def __init__(self, pname, price):
        self.pname = pname
        self.price = price

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_product(self, product):
        self.items.append(product)
        print(f"{product.pname} added to cart.")

    def remove_product(self, product):
        self.items.remove(product)
        print(f"{product.pname} removed from cart.")

    def get_total(self):
        return sum(item.price for item in self.items)

    def show_cart(self):
        print("\nCart Items:")
        for item in self.items:
            print(f"- {item.pname}: Rs.{item.price}")
        print("Total:", self.get_total())

class Coupon:
    def __init__(self, code, discount):
        self.code = code
        self.discount = discount

    def apply_discount(self, total):
        return total - (total * self.discount / 100)


class Order:
    def __init__(self, cart, coupon=None):
        self.cart = cart
        self.coupon = coupon

    def final_price(self):
        total = self.cart.get_total()
        if self.coupon:
            total = self.coupon.apply_discount(total)
        return total


class PaymentProcessor(ABC):

    @abstractmethod
    def process_payment(self, amount):
        pass


class CreditCard(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing Rs.{amount} via Credit Card.")


class Paypal(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing Rs.{amount} via PayPal.")


class Crypto(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing Rs.{amount} via Crypto.")


def ecom():
    # Products
    p1 = Product("Laptop", 50000)
    p2 = Product("Mouse", 1000)
    p3 = Product("Keyboard", 2000)

    cart = ShoppingCart()
    coupon = None
    coupon_used = False  

    while True:
        print("\n===== E-COMMERCE MENU =====")
        print("1. Add Product")
        print("2. View Cart")
        print("3. Apply Coupon")
        print("4. Checkout")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nAvailable Products:")
            print("1. Laptop - 50000")
            print("2. Mouse - 1000")
            print("3. Keyboard - 2000")

            p_choice = input("Select product: ")

            if p_choice == "1":
                cart.add_product(p1)
            elif p_choice == "2":
                cart.add_product(p2)
            elif p_choice == "3":
                cart.add_product(p3)
            else:
                print("Invalid product choice")

        elif choice == "2":
            cart.show_cart()

        elif choice == "3":
            if coupon_used:  
                print("You are not eligible for coupon.")
                continue

            code = input("Enter coupon code: ")
            if code == "SAVE10":
                coupon = Coupon("SAVE10", 10)
                coupon_used = True   
                print("Coupon applied!")
            else:
                print("Invalid coupon")

        elif choice == "4":
            if not cart.items:
                print("Cart is empty!")
                continue

            order = Order(cart, coupon)
            amount = order.final_price()
            print(f"\nFinal Amount: Rs.{amount}")

            print("\nSelect Payment Method:")
            print("1. Credit Card")
            print("2. PayPal")
            print("3. Crypto")

            pay_choice = input("Enter choice: ")

            if pay_choice == "1":
                payment = CreditCard()
            elif pay_choice == "2":
                payment = Paypal()
            elif pay_choice == "3":
                payment = Crypto()
            else:
                print("Invalid payment method")
                continue

            payment.process_payment(amount)
            print("Order placed successfully!")
            break

        elif choice == "5":
            print("Thank you for visiting!")
            break

        else:
            print("Invalid choice. Try again.")

ecom()