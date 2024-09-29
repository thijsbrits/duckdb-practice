from dataclasses import dataclass, fields
from app.utils import convert_empty_to_none
import re

class UnrealisticModelYearError(Exception):
    pass

class InvalidLocationFormatError(Exception):
    pass

class InvalidStateError(Exception):
    pass

class InvalidVinSizeError(Exception):
    pass


@dataclass
class ElectricVehicle:
    vin_first10: str
    county: str
    city: str
    state: str
    postal_code: str
    model_year: int
    make: str
    model: str
    electric_vehicle_type: str
    cafv_eligibility: str
    electric_range: int
    base_msrp: int
    legislative_district: int
    dol_vehicle_id: int
    vehicle_location: str  # Note: we load it as string as we use validation to ensure the format
    electric_utility: str
    census_tract: str

    def __post_init__(self):
        if not len(self.vin_first10) == 10:
            raise InvalidVinSizeError(f"Invalid VIN (1-10): {self.vin_first10}, should be 10 characters")

        if not len(self.state) == 2:
            raise InvalidStateError(f"Invalid state {self.state}, state should be 2 letters")

        if (self.model_year < 1700) or self.model_year > 3000:
            raise UnrealisticModelYearError(f"Non-realistic model_year {self.model_year}")

        if self.vehicle_location and not re.match(r'POINT \((\-?\d+\.\d+) (\-?\d+\.\d+)\)', self.vehicle_location):
            raise InvalidLocationFormatError(
                f"Invalid location format {self.vehicle_location}, should be in format POINT (0.00, 0.00)")

        # we can add more data validations here...

    @classmethod
    def from_dict(cls, obj):
        obj = {key: convert_empty_to_none(value) for key, value in obj.items()}

        return cls(
            vin_first10=obj['VIN (1-10)'],
            county=obj['County'],
            city=obj['City'],
            state=obj['State'],
            postal_code=obj['Postal Code'],
            model_year=int(obj['Model Year']) if obj['Model Year'] else None,
            make=obj['Make'],
            model=obj['Model'],
            electric_vehicle_type=obj['Electric Vehicle Type'],
            cafv_eligibility=obj['Clean Alternative Fuel Vehicle (CAFV) Eligibility'],
            electric_range=int(obj['Electric Range']) if obj['Electric Range'] else None,
            base_msrp=int(obj['Base MSRP']) if obj['Base MSRP'] else None,
            legislative_district=int(obj['Legislative District']) if obj['Legislative District'] else None,
            dol_vehicle_id=int(obj['DOL Vehicle ID']) if obj['DOL Vehicle ID'] else None,
            vehicle_location=obj['Vehicle Location'],
            electric_utility=obj['Electric Utility'],
            census_tract=obj['2020 Census Tract'],
        )

    @classmethod
    def field_names(cls):
        return tuple(field.name for field in fields(cls))
