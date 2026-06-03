from abc import ABC, abstractmethod
import requests


class BaseAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> tuple:
        """Получает координаты страны (boundingbox)"""
        pass

    @abstractmethod
    def get_aeroplanes(self, country_name: str) -> list:
        """Получает список самолётов над страной"""
        pass


class AeroplanesAPI(BaseAPI):
    """Класс для работы с API nominatim и opensky"""

    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"

    def get_country_coordinates(self, country_name: str) -> tuple:
        """Получает boundingbox страны (юг, север, запад, восток)"""
        params = {
            "q": country_name,
            "format": "json",
            "limit": 1,
            "accept-language": "en"
        }
        try:
            # Добавляем заголовок User-Agent, чтобы API нас не блокировал
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
            }
            response = requests.get(self.nominatim_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if data:
                boundingbox = data[0].get("boundingbox", [])
                if boundingbox:
                    return (
                        float(boundingbox[0]),  # юг
                        float(boundingbox[1]),  # север
                        float(boundingbox[2]),  # запад
                        float(boundingbox[3])   # восток
                    )
        except (requests.RequestException, ValueError, KeyError, IndexError) as e:
            print(f"Ошибка при получении координат: {e}")
        return (0, 0, 0, 0)

    def get_aeroplanes(self, country_name: str) -> list:
        """Получает список самолётов над страной"""
        coords = self.get_country_coordinates(country_name)
        print(f"Координаты страны: {coords}")

        if coords == (0, 0, 0, 0):
            print("Координаты не найдены")
            return []

        south, north, west, east = coords
        params = {
            "lamin": south,
            "lamax": north,
            "lomin": west,
            "lomax": east
        }
        print(f"Параметры запроса: {params}")

        try:
            response = requests.get(self.opensky_url, params=params)
            print(f"Статус ответа: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            states = data.get("states", [])
            print(f"Найдено самолётов: {len(states)}")
            return states
        except requests.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return []