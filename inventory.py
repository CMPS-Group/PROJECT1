def levenshtein_distance(s1, s2):
    """Calculates the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

class Inventory:
    def __init__(self):
        self.cars = {}

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

    def find_car_by_vin_fuzzy(self, search_vin: str):
        """
        Finds the car with the most similar VIN using Levenshtein distance.
        Returns a tuple of (car, distance).
        """
        if not self.cars:
            return None, float('inf')

        best_match_car = None
        min_distance = float('inf')

        for vin, car in self.cars.items():
            distance = levenshtein_distance(search_vin.upper(), vin)
            if distance < min_distance:
                min_distance = distance
                best_match_car = car
        
        return best_match_car, min_distance

    def find_car_by_make_and_model(self, make, model):
        """Finds cars by make and model."""
        return [car for car in self.cars.values() if car.make.lower() == make.lower() and car.model.lower() == model.lower()]