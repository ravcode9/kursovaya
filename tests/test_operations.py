import json
import pytest
from src.operations import read_operations_from_json, format_operation, display_last_operations


@pytest.fixture
def temp_json_file(tmp_path):
    # Создаем временный файл с тестовыми данными
    data = [{'date': '2023-11-27T12:34:56.789', 'description': 'Тестовая операция', 'from': '1234567890123456',
             'to': '9876543210123456', 'operationAmount': {'amount': '100', 'currency': {'name': 'USD'}}}]
    json_data = json.dumps(data)
    file_path = tmp_path / 'test_operations.json'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_data)
    return file_path


def test_read_operations_from_json(temp_json_file):
    # Тестируем функцию read_operations_from_json
    result = read_operations_from_json(temp_json_file)
    assert result == [
        {'date': '2023-11-27T12:34:56.789', 'description': 'Тестовая операция', 'from': '1234567890123456',
         'to': '9876543210123456', 'operationAmount': {'amount': '100', 'currency': {'name': 'USD'}}}]


def test_format_operation():
    # Тестируем функцию format_operation на примере операции
    operation = {'date': '2023-11-27T12:34:56.789', 'description': 'Тестовая операция', 'from': '1234567890123456',
                 'to': '9876543210123456', 'operationAmount': {'amount': '100', 'currency': {'name': 'USD'}}}
    expected_result = "27.11.2023 Тестовая операция\n1234 XX** **** 3456 -> **3456\n100 USD\n"
    result = format_operation(operation)
    assert result == expected_result