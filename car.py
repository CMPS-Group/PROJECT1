# car.py
# (Use the Car class implementation you already have here)
from dataclasses import dataclass, field
from datetime import date
from typing import Optional, ClassVar, Dict

class PermissionError(Exception):
    pass

class VINExistsError(ValueError):
    pass

@dataclass
class Car:
    vin: str
    year: int
    make: str
    model: str
    colour: str
    price: float
    delivery_date: Optional[date] = None

    sold: bool = field(default=False, init=False)
    sold_date: Optional[date] = field(default=None, init=False)

    _registry: ClassVar[Dict[str, "Car"]] = {}

    def __post_init__(self):
        vin = self.vin.strip().upper()
        if not vin:
            raise ValueError("VIN must be a non-empty string.")
        if vin in Car._registry:
            raise VINExistsError(f"VIN {vin} already exists.")
        if self.price < 0:
            raise ValueError("Price must be >= 0.")
        self.vin = vin
        Car._registry[vin] = self

    def __repr__(self) -> str:
        status = "Sold" if self.sold else "Available"
        return f"<Car {self.vin} {self.year} {self.make} {self.model} {self.colour} ${self.price:.2f} {status}>"

    def is_available(self) -> bool:
        return not self.sold

    def get_sold_date(self):
        return self.sold_date

    def to_dict(self):
        return {
            "vin": self.vin, "year": self.year, "make": self.make,
            "model": self.model, "colour": self.colour, "price": self.price,
            "delivery_date": self.delivery_date, "sold": self.sold, "sold_date": self.sold_date
        }

    def sell(self, sold_on: Optional[date] = None):
        if self.sold:
            raise ValueError("Car is already sold.")
        self.sold = True
        self.sold_date = sold_on or date.today()

    def mark_available(self):
        if not self.sold:
            return
        self.sold = False
        self.sold_date = None

    def _require_admin(self, admin: bool):
        if not admin:
            raise PermissionError("Admin privileges required for this operation.")

    def update_price(self, new_price: float, admin: bool = False):
        self._require_admin(admin)
        if new_price < 0:
            raise ValueError("Price must be >= 0.")
        self.price = float(new_price)

    def update_make(self, new_make: str, admin: bool = False):
        self._require_admin(admin)
        if not new_make:
            raise ValueError("Make must be non-empty.")
        self.make = new_make

    def update_model(self, new_model: str, admin: bool = False):
        self._require_admin(admin)
        if not new_model:
            raise ValueError("Model must be non-empty.")
        self.model = new_model

    def update_colour(self, new_colour: str, admin: bool = False):
        self._require_admin(admin)
        if not new_colour:
            raise ValueError("Colour must be non-empty.")
        self.colour = new_colour

    def update_year(self, new_year: int, admin: bool = False):
        self._require_admin(admin)
        if new_year <= 0:
            raise ValueError("Year must be a positive integer.")
        self.year = int(new_year)

    def update_availability(self, available: bool, admin: bool = False, sold_on: Optional[date] = None):
        self._require_admin(admin)
        if available:
            self.mark_available()
        else:
            if self.sold:
                return
            self.sell(sold_on=sold_on)

    def delete(self, admin: bool = False):
        self._require_admin(admin)
        Car._registry.pop(self.vin, None)

    def is_delivery_expired(self, ref_date: Optional[date] = None) -> bool:
        if self.delivery_date is None:
            return False
        ref = ref_date or date.today()
        return self.delivery_date < ref

    @classmethod
    def cleanup_expired(cls, ref_date: Optional[date] = None) -> int:
        ref = ref_date or date.today()
        to_delete = [vin for vin, car in cls._registry.items() if car.delivery_date is not None and car.delivery_date < ref]
        for vin in to_delete:
            cls._registry.pop(vin, None)
        return len(to_delete)

    @classmethod
    def get_by_vin(cls, vin: str):
        return cls._registry.get(vin.strip().upper())

    @classmethod
    def all_cars(cls):
        return dict(cls._registry)