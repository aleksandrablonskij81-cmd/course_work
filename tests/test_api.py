from src.api import AeroplanesAPI


def test_get_country_coordinates():
    api = AeroplanesAPI()
    coords = api.get_country_coordinates("Germany")
    assert len(coords) == 4
    assert coords != (0, 0, 0, 0)

from src.api import AeroplanesAPI


def test_get_country_coordinates():
    api = AeroplanesAPI()
    coords = api.get_country_coordinates("Germany")
    assert len(coords) == 4
    assert coords != (0, 0, 0, 0)


def test_get_country_coordinates_invalid():
    """Тест: несуществующая страна"""
    api = AeroplanesAPI()
    coords = api.get_country_coordinates("NonExistentCountry12345")
    assert coords == (0, 0, 0, 0)


def test_get_aeroplanes():
    """Тест: получение самолётов"""
    api = AeroplanesAPI()
    planes = api.get_aeroplanes("Germany")
    assert isinstance(planes, list)
