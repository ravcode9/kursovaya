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


def test_display_last_operations(temp_json_file, capfd):
    # Тестируем функцию display_last_operations на примере операций
    operations = [
        {'date': '2023-11-27T12:34:56.789', 'description': 'Тестовая операция1', 'from': '1234567890123456',
         'to': '9876543210123456', 'operationAmount': {'amount': '100', 'currency': {'name': 'USD'}}},
        {'date': '2023-11-26T10:00:00.000', 'description': 'Тестовая операция2', 'from': '9876543210123456',
         'to': '1234567890123456', 'operationAmount': {'amount': '50', 'currency': {'name': 'EUR'}}},
    ]

    # Тестируем функцию display_last_operations
    display_last_operations(operations)

    # Захватываем выведенный результат
    captured = capfd.readouterr()
    expected_output = "27.11.2023 Тестовая операция1\n1234 XX** **** 3456 -> **3456\n100 USD\n\n\n26.11.2023 Тестовая операция2\n9876 XX** **** 3456 -> **3456\n50 EUR\n"
    assert captured.out.strip() == expected_output.strip()


def test_format_invalid_operation():
    # Тестируем функцию format_operation на недействительной операции
    invalid_operation = {}
    expected_result = "Недействительная операция"
    result = format_operation(invalid_operation)
    assert result == expected_result


def test_format_operation_invalid_data():
    # Тестируем функцию format_operation на недействительных данных
    invalid_operation = {'date': '2023-11-27T12:34:56.789'}
    expected_result = "Недействительная операция"
    result = format_operation(invalid_operation)
    assert result == expected_result


def test_read_operations_from_json_empty_file(tmp_path):
    # Создаем пустой временный файл
    file_path = tmp_path / 'empty_operations.json'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('')

    result = read_operations_from_json(file_path)
    assert result == []


def test_format_operation_missing_keys():
    # Тестируем функцию format_operation на операции с отсутствующими ключами
    invalid_operation = {'date': '2023-11-27T12:34:56.789'}
    expected_result = "Недействительная операция"
    result = format_operation(invalid_operation)
    assert result == expected_result

    invalid_operation = {'description': 'Тестовая операция'}
    expected_result = "Недействительная операция"
    result = format_operation(invalid_operation)
    assert result == expected_result


def test_display_last_operations_no_operations(capfd):
    # Тестируем функцию display_last_operations без операций
    display_last_operations([])
    captured = capfd.readouterr()
    assert captured.out.strip() == "Операции не найдены."

def test_display_last_operations_less_than_5_operations(capfd):
    # Тестируем функцию display_last_operations с менее чем 5 операциями
    operations = [
        {'date': '2023-11-27T12:34:56.789', 'description': 'Тестовая операция1', 'from': '1234567890123456',
         'to': '9876543210123456', 'operationAmount': {'amount': '100', 'currency': {'name': 'USD'}}},
    ]
    display_last_operations(operations)
    captured = capfd.readouterr()
    assert "27.11.2023 Тестовая операция1" in captured.out