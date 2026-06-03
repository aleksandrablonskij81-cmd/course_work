from typing import List


class Aeroplane:
    """Класс самолёта с атрибутами и методами сравнения"""

    def __init__(self, icao24: str, callsign: str, origin_country: str,
                 velocity: float, altitude: float):
        self.icao24 = icao24
        self.callsign = callsign.strip() if callsign else "Unknown"
        self.origin_country = origin_country
        self.velocity = float(velocity) if velocity else 0.0
        self.altitude = float(altitude) if altitude else 0.0

    def __str__(self) -> str:
        return (f"Самолёт: {self.callsign}, Страна: {self.origin_country}, "
                f"Скорость: {self.velocity} м/с, Высота: {self.altitude} м")

    def __lt__(self, other: "Aeroplane") -> bool:
        """Меньше по скорости"""
        return self.velocity < other.velocity

    def __gt__(self, other: "Aeroplane") -> bool:
        """Больше по скорости"""
        return self.velocity > other.velocity

    def __le__(self, other: "Aeroplane") -> bool:
        return self.velocity <= other.velocity

    def __ge__(self, other: "Aeroplane") -> bool:
        return self.velocity >= other.velocity

    def __eq__(self, other: "Aeroplane") -> bool:
        return self.velocity == other.velocity

    @classmethod
    def cast_to_object_list(cls, data: list) -> List["Aeroplane"]:
        """Преобразует список данных в список объектов Aeroplane"""
        aeroplanes = []
        for item in data:
            if len(item) >= 7:
                try:
                    aeroplane = cls(
                        icao24=item[0],
                        callsign=item[1],
                        origin_country=item[2],
                        velocity=item[9] if item[9] else 0,
                        altitude=item[7] if item[7] else 0
                    )
                    aeroplanes.append(aeroplane)
                except (ValueError, TypeError):
                    continue
        return aeroplanes

    def to_dict(self) -> dict:
        """Возвращает словарь с данными самолёта для сохранения в JSON"""
        return {
            "icao24": self.icao24,
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "velocity": self.velocity,
            "altitude": self.altitude
        }
