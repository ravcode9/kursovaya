import json
from datetime import datetime


def read_operations_from_json(file_path):
    with open(file_path, 'r', encoding='Utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []  # Возвращаем пустой список в случае ошибки декодирования JSON
    return data


if __name__ == "__main__":
    file_path = "C:/Users/ralatypov/Downloads/operations.json"
    operations = read_operations_from_json(file_path)