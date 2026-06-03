import pytest
from src.aeroplane import Aeroplane


def test_aeroplane_creation():
    plane = Aeroplane("abc123", "UAL123", "USA", 250.5, 10000.0)
    assert plane.icao24 == "abc123"
    assert plane.callsign == "UAL123"
    assert plane.origin_country == "USA"
    assert plane.velocity == 250.5
    assert plane.altitude == 10000.0


def test_aeroplane_comparison():
    plane1 = Aeroplane("a", "A", "USA", 200, 5000)
    plane2 = Aeroplane("b", "B", "USA", 300, 10000)
    assert plane1 < plane2
    assert plane2 > plane1


def test_cast_to_object_list():
    data = [
        ["abc", "UAL123", "USA", None, None, None, None, 10000, None, 250.0],
        ["def", None, "Russia", None, None, None, None, 8000, None, 200.0]
    ]
    planes = Aeroplane.cast_to_object_list(data)
    assert len(planes) == 2
    assert planes[0].callsign == "UAL123"
    assert planes[1].origin_country == "Russia"
