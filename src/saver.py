from abc import ABC, abstractmethod
import json
import os
from typing import List
from src.aeroplane import Aeroplane


class BaseSaver(ABC):
    """Абстрактный класс для сохранения данных"""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолёт в хранилище"""
        pass

    @abstractmethod
    def get_aeroplanes(self, **criteria) -> List[Aeroplane]:
        """Получает самолёты по критериям"""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолёт из хранилища"""
        pass


class JSONSaver(BaseSaver):
    """Сохраняет данные в JSON-файл"""

    def __init__(self, filename: str = "aeroplanes.json"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Создаёт файл, если его нет"""
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _load_data(self) -> list:
        """Загружает данные из файла"""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, ValueError):
            return []

    def _save_data(self, data: list) -> None:
        """Сохраняет данные в файл"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолёт в файл"""
        data = self._load_data()
        aeroplane_dict = aeroplane.to_dict()
        # Проверяем, нет ли уже такого самолёта (по icao24)
        for existing in data:
            if existing.get("icao24") == aeroplane_dict["icao24"]:
                return
        data.append(aeroplane_dict)
        self._save_data(data)

    def get_aeroplanes(self, **criteria) -> List[Aeroplane]:
        """Получает самолёты по критериям (например, origin_country='Russia')"""
        data = self._load_data()
        result = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                try:
                    aeroplane = Aeroplane(
                        icao24=item["icao24"],
                        callsign=item["callsign"],
                        origin_country=item["origin_country"],
                        velocity=item["velocity"],
                        altitude=item["altitude"]
                    )
                    result.append(aeroplane)
                except (KeyError, ValueError, TypeError):
                    continue
        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолёт из файла"""
        data = self._load_data()
        data = [item for item in data if item.get("icao24") != aeroplane.icao24]
        self._save_data(data)