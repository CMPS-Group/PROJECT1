# ============================================================
# main.py - E-Commerce Dealership Simulation (Vanja Tilinger)
# ============================================================

from car import Car, Inventory


#  SIMULATION 

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role_type = role
        self.full_name = None 

    def login(self):
        pw = input(f"Password for {self.username}: ").strip()
        if pw == self.password:
            print(f" Welcome {self.role_type}!")
            if self.role_type == "Buyer" and not self.full_name:
                self.full_name = input("Please enter your name for the order: ").strip().title()
            return self.role_type
        else:
            print("Invalid credentials.")
            return None


class Cart:
    def __init__(self):
        self.cartItems = []

    def addCar(self, car):
        self.cartItems.append(car)
        print(f"Added {car.make} {car.model} to cart.")

    def displayCart(self):
        print("\n Your Cart:")
        for car in self.cartItems:
            print(car)

    def calculateTotal(self):
        return sum(car.price for car in self.cartItems)


class Payment:
    def processPayment(self, total):
        print(f"\n Total amount due: ${total}")
        card = input("Enter mock card number (Please input 8 numbers): ")
        if len(card) >= 8:
            print(" Payment successful!")
            return True
        else:
            print("Payment failed. Invalid card.")
            return False


class Delivery:
    def scheduleDelivery(self):
        print("\n Scheduling delivery...")
        date = input("Enter desired delivery date: ")
        print(f"Delivery scheduled for {date}.\n")


# --- MAIN PROGRAM ---
def mainProgram():
    print("========================================")
    print("   E-Commerce Car Dealership Simulation  ")
    print("========================================\n")

    # Users
    admin = User("admin", "1234", "Admin")
    seller = User("seller", "5678", "Seller")
    buyer = User("buyer", "9999", "Buyer")
    users = {"admin": admin, "seller": seller, "buyer": buyer}

    # Inventory
    inventory = Inventory()
    inventory.add_car(Car("VIN101", 2022, "Toyota", "Camry", "Silver", 28000))
    inventory.add_car(Car("VIN202", 2023, "Honda", "Civic", "Blue", 25000))
    inventory.add_car(Car("VIN303", 2023, "Ford", "Escape", "White", 32000))

    # Main loop
    logged_in_role = None
    selection = ""

    while selection != "4":
        print("\nMAIN MENU:")
        print("1. LOGIN")
        print("2. VIEW INVENTORY")
        print("3. BUY")
        print("4. EXIT")

        selection = input("Choose an option (1-4): ").strip().upper()

        #  LOGIN 
        if selection == "1":
            name = input("Enter username: ").strip().lower()
            user = users.get(name)
            if user:
                role = user.login()
                if role:
                    logged_in_role = role
                    current_user = user
            else:
                print("Unknown user.")

        #  VIEW INVENTORY 
        elif selection == "2":
            print("\nCURRENT INVENTORY:")
            print(inventory.list_inventory())

            if logged_in_role in ["Admin", "Seller"]:
                print("\n MANAGE INVENTORY OPTIONS:")
                print("1. CREATE (Admin Only)")
                print("2. UPDATE PRICE")
                print("3. REMOVE (Admin Only)")
                print("4. BACK")
                action = input("Select option: ").strip().upper()
                if action == "1" and logged_in_role == "Admin":
                    vin = input("VIN: ")
                    year = int(input("Year: "))
                    make = input("Make: ")
                    model = input("Model: ")
                    colour = input("Colour: ")
                    price = float(input("Price: "))
                    print(inventory.add_car(Car(vin, year, make, model, colour, price)))
                elif action == "2" and logged_in_role in ["Admin", "Seller"]:
                    vin = input("Enter VIN to update: ")
                    car = inventory.find_car(vin)
                    if car:
                        new_price = float(input("New price: "))
                        car.price = new_price
                        print("Price updated.")
                    else:
                        print("Car not found.")
                elif action == "3" and logged_in_role == "Admin":
                    vin = input("Enter VIN to remove: ")
                    print(inventory.remove_car(vin))
                elif action == "4":
                    continue
                else:
                    print("Invalid action or insufficient permissions.")

        #  BUY 
        elif selection == "3":
            if not logged_in_role:
                print("You must log in first, press OPTION: 1")
                continue

            if logged_in_role != "Buyer":
                print(" Only buyers can purchase vehicles.")
                continue

            print("\nAvailable vehicles:")
            print(inventory.list_inventory())
            vin = input("Enter VIN to purchase: ")
            car = inventory.find_car(vin)

            if car:
                cart = Cart()
                cart.addCar(car)
                total = cart.calculateTotal()
                cart.displayCart()
                pay = Payment()
                if pay.processPayment(total):
                    delivery = Delivery()
                    delivery.scheduleDelivery()
                    print("Purchase complete! Thank you for shopping,", current_user.full_name or current_user.username) 
                    selection = "EXIT"
            else:
                print("Car not found.")

        elif selection == "EXIT":
            print("\n Thanks for using our service!")

        else:
            print("Invalid selection. Please try again.")

    print("\nProgram ended.")


if __name__ == "__main__":
    mainProgram()
