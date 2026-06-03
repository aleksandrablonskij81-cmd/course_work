import os
import json
import pytest
from src.aeroplane import Aeroplane
from src.saver import JSONSaver


def test_json_saver_add_and_get():
    """Тест: добавление и получение самолёта"""
    filename = "test_aeroplanes.json"
    saver = JSONSaver(filename)
    plane = Aeroplane("abc123", "TEST", "USA", 250.5, 10000.0)
    saver.add_aeroplane(plane)

    result = saver.get_aeroplanes(icao24="abc123")
    assert len(result) == 1
    assert result[0].callsign == "TEST"

    # Удаляем тестовый файл
    if os.path.exists(filename):
        os.remove(filename)


def test_json_saver_delete():
    """Тест: удаление самолёта"""
    filename = "test_aeroplanes.json"
    saver = JSONSaver(filename)
    plane = Aeroplane("abc123", "TEST", "USA", 250.5, 10000.0)
    saver.add_aeroplane(plane)
    saver.delete_aeroplane(plane)

    result = saver.get_aeroplanes(icao24="abc123")
    assert len(result) == 0

    # Удаляем тестовый файл
    if os.path.exists(filename):
        os.remove(filename)


def test_json_saver_get_empty():
    """Тест: получение из пустого файла"""
    filename = "test_empty.json"
    if os.path.exists(filename):
        os.remove(filename)

    saver = JSONSaver(filename)
    result = saver.get_aeroplanes()
    assert result == []

    if os.path.exists(filename):
        os.remove(filename)
