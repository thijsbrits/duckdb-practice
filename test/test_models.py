from models import ElectricVehicle, UnrealisticModelYearError, InvalidStateError, InvalidLocationFormatError, InvalidVinSizeError
import pytest
import copy

@pytest.fixture
def electric_vehicle_data():
    return {'VIN (1-10)': '5YJ3E1EB4L', 'County': 'Yakima', 'City': 'Yakima', 'State': 'WA', 'Postal Code': '98908', 'Model Year': '2020', 'Make': 'TESLA', 'Model': 'MODEL 3', 'Electric Vehicle Type': 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle (CAFV) Eligibility': 'Clean Alternative Fuel Vehicle Eligible', 'Electric Range': '322', 'Base MSRP': '0', 'Legislative District': '14', 'DOL Vehicle ID': '127175366', 'Vehicle Location': 'POINT (-120.56916 46.58514)', 'Electric Utility': 'PACIFICORP', '2020 Census Tract': '53077000904'}


@pytest.fixture
def ev_data_missing_element(electric_vehicle_data):
    changed_ev = copy.deepcopy(electric_vehicle_data)
    del changed_ev['VIN (1-10)']
    return changed_ev

@pytest.fixture
def ev_data_incorrect_vin_format(electric_vehicle_data):
    changed_ev = copy.deepcopy(electric_vehicle_data)
    changed_ev['VIN (1-10)'] = '5YJ3E1EB4L____'
    return changed_ev

@pytest.fixture
def ev_data_incorrect_location_format(electric_vehicle_data):
    changed_ev = copy.deepcopy(electric_vehicle_data)
    # should have POINT prefix
    changed_ev['Vehicle Location'] = '(-120.56916 46.58514)'
    return changed_ev

@pytest.fixture
def ev_data_unrealistic_model_year(electric_vehicle_data):
    changed_ev = copy.deepcopy(electric_vehicle_data)
    changed_ev['Model Year'] = 9999
    return changed_ev

@pytest.fixture
def ev_invalid_state(electric_vehicle_data):
    changed_ev = copy.deepcopy(electric_vehicle_data)
    changed_ev['State'] = "sdfghjk"
    return changed_ev


@pytest.fixture
def ev_data_int_conversion_fail(electric_vehicle_data):
    changed_ev = copy.deepcopy(electric_vehicle_data)
    changed_ev['Base MSRP'] = 'some_string'
    return changed_ev


def test_electric_vehicle(electric_vehicle_data):
    ElectricVehicle.from_dict(electric_vehicle_data)


def test_missing_element(ev_data_missing_element):
    with pytest.raises(KeyError):
        ElectricVehicle.from_dict(ev_data_missing_element)


def test_incorrect_vin_format(ev_data_incorrect_vin_format):
    with pytest.raises(InvalidVinSizeError):
        ElectricVehicle.from_dict(ev_data_incorrect_vin_format)


def test_incorrect_location_format(ev_data_incorrect_location_format):
    with pytest.raises(InvalidLocationFormatError):
        ElectricVehicle.from_dict(ev_data_incorrect_location_format)


def test_unrealistic_model_year(ev_data_unrealistic_model_year):
    with pytest.raises(UnrealisticModelYearError):
        ElectricVehicle.from_dict(ev_data_unrealistic_model_year)


def test_invalid_state(ev_invalid_state):
    with pytest.raises(InvalidStateError):
        ElectricVehicle.from_dict(ev_invalid_state)


def test_type_conversion_fail(ev_data_int_conversion_fail):
    with pytest.raises(ValueError):
        ElectricVehicle.from_dict(ev_data_int_conversion_fail)