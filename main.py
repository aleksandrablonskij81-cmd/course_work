from src.api import AeroplanesAPI
from src.aeroplane import Aeroplane
from src.saver import JSONSaver


def user_interaction():
    """Основная функция взаимодействия с пользователем"""

    print("✈️ Добро пожаловать в систему мониторинга самолётов!")
    print("-" * 50)

    # Шаг 1: ввод страны
    country = input("Введите название страны для поиска самолётов: ").strip()
    if not country:
        print("Ошибка: название страны не может быть пустым")
        return

    # Шаг 2: получаем данные через API
    print(f"\n🔍 Ищем самолёты над страной '{country}'...")
    api = AeroplanesAPI()
    raw_data = api.get_aeroplanes(country)

    if not raw_data:
        print("❌ Не удалось получить данные о самолётах. Проверьте название страны или подключение к интернету.")
        return

    # Шаг 3: преобразуем в объекты
    print("Преобразуем данные в объекты...")
    aeroplanes = Aeroplane.cast_to_object_list(raw_data)
    print(f"✅ Найдено {len(aeroplanes)} самолётов.")

    if not aeroplanes:
        print("Нет данных о самолётах в этом регионе.")
        return

    # Шаг 4: сохраняем в JSON
    print("Сохраняем данные в JSON...")
    try:
        saver = JSONSaver("aeroplanes.json")
        for i, plane in enumerate(aeroplanes):
            saver.add_aeroplane(plane)
            if i % 1000 == 0:
                print(f"Сохранено {i} самолётов...")
        print(f"💾 Данные сохранены в файл aeroplanes.json")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
        return

    # Шаг 5: запрос топ N по высоте
    print("\n" + "-" * 50)
    try:
        top_n = int(input("Введите количество самолётов для вывода в топ N (по высоте): "))
        if top_n <= 0:
            print("Количество должно быть положительным. Вывожу топ-5.")
            top_n = 5
    except ValueError:
        print("Некорректный ввод. Вывожу топ-5.")
        top_n = 5

    # Сортируем по высоте (убывание)
    sorted_by_altitude = sorted(aeroplanes, key=lambda p: p.altitude, reverse=True)
    top_aeroplanes = sorted_by_altitude[:top_n]

    print(f"\n🏆 Топ-{top_n} самолётов по высоте полёта:")
    for i, plane in enumerate(top_aeroplanes, 1):
        print(f"{i}. {plane}")

    # Шаг 6: фильтрация по стране регистрации
    print("\n" + "-" * 50)
    filter_country = input("Введите страну для фильтрации самолётов (или оставьте пустым): ").strip()
    if filter_country:
        filtered = [p for p in aeroplanes if filter_country.lower() in p.origin_country.lower()]
        print(f"\n✈️ Самолёты из страны '{filter_country}':")
        if filtered:
            for i, plane in enumerate(filtered, 1):
                print(f"{i}. {plane}")
        else:
            print(f"Самолётов из страны '{filter_country}' не найдено.")

    print("\n" + "=" * 50)
    print("Программа завершена. Хорошего дня!")


if __name__ == "__main__":
    user_interaction()
