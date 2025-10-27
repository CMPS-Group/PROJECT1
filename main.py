from car import Car, VINExistsError
from inventory import Inventory

def print_menu():
    """Prints the main menu options to the console."""
    print("\n--- Car Inventory Management ---")
    print("1. Add a new car")
    print("2. List all cars")
    print("3. Find a car by VIN")
    print("4. Find cars by make and model")
    print("5. Sell a car")
    print("6. Remove a car")
    print("7. Exit")

def main():
    """Main function to run the car inventory application."""
    inventory = Inventory()

    # Pre-populate with some data for demonstration
    try:
        inventory.add_car(Car(vin="VIN123", year=2021, make="Honda", model="Civic", colour="Blue", price=22000.0))
        inventory.add_car(Car(vin="VIN456", year=2022, make="Ford", model="Mustang", colour="Red", price=45000.0))
    except VINExistsError as e:
        print(f"Error pre-populating data: {e}")


    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            try:
                vin = input("Enter car VIN: ")
                make = input("Enter car make: ")
                model = input("Enter car model: ")
                year = int(input("Enter car year: "))
                colour = input("Enter car colour: ")
                price = float(input("Enter car price: "))
                new_car = Car(vin=vin, make=make, model=model, year=year, colour=colour, price=price)
                print(inventory.add_car(new_car))
            except ValueError:
                print("Invalid input. Year must be an integer and price must be a number.")
            except VINExistsError as e: # type: ignore
                print(f"Error: {e}")

        elif choice == '2':
            print("\n--- Current Inventory ---")
            print(inventory.list_inventory())

        elif choice == '3':
            vin = input("Enter car VIN to find: ")
            found_car = inventory.find_car(vin)
            if found_car:
                print("\n--- Car Found ---")
                print(found_car)
            else:
                print("Car not found. Searching for the closest match...")
                best_match, distance = inventory.find_car_by_vin_fuzzy(vin)
                
                # Only suggest a match if it's reasonably close (e.g., distance <= 3)
                if best_match and distance <= 3:
                    print(f"Did you mean this car? (VIN: {best_match.vin})")
                    print(best_match)
                    confirm = input("Is this the correct car? (y/n): ").lower()
                    if confirm == 'y':
                        # You can add logic here to proceed with the found car
                        print("Confirmed.")
                    else:
                        print("Search cancelled.")
                else:
                    print("No close match found in inventory.")

        elif choice == '4':
            make = input("Enter car make to find: ")
            model = input("Enter car model to find: ")
            found_cars = inventory.find_car_by_make_and_model(make, model)
            if found_cars:
                print("\n--- Cars Found ---")
                for car in found_cars:
                    print(car)
            else:
                print("No cars found with that make and model.")

        elif choice == '5':
            vin = input("Enter VIN of car to sell: ")
            car_to_sell = inventory.find_car(vin)
            if car_to_sell:
                try:
                    car_to_sell.sell()
                    print(f"Car {vin} marked as sold.")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Car not found.")

        elif choice == '6':
            vin = input("Enter VIN of car to remove: ")
            print(inventory.remove_car(vin))

        elif choice == '7':
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()