import os.path
import json

def save_state(key: str = '', value = None) -> None:
    data = {}
    if key and value:
        data[key] = value

    with open(os.path.join(os.getcwd(), "app", "app.json"), 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def get_state() -> dict:
    try:
        with open(os.path.join(os.getcwd(), "app", "app.json"), encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f'Ошибка открытия state: {e}')
