class Inventory:
    def __init__(self):
        self.cars = {}  # key: VIN, value: Car object

    def add_car(self, car):
        if car.vin in self.cars:
            return f"Car with VIN {car.vin} already exists."
        self.cars[car.vin] = car
        return f"Car with VIN {car.vin} added successfully."

    def remove_car(self, vin):
        if vin in self.cars:
            del self.cars[vin]
            return f"Car with VIN {vin} removed."
        return f"Car with VIN {vin} not found."

    def update_car(self, vin, **kwargs):
        car = self.cars.get(vin)
        if not car:
            return f"Car with VIN {vin} not found."
        for key, value in kwargs.items():
            if hasattr(car, key):
                setattr(car, key, value)
        return f"Car with VIN {vin} updated."

    def list_inventory(self):
        if not self.cars:
            return "Inventory is empty."
        return "\n".join(str(car) for car in self.cars.values())

    def find_car(self, vin):
        return self.cars.get(vin)