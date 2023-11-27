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


def format_operation(operation):
    if 'date' not in operation or 'operationAmount' not in operation:
        return "Недействительная операция"

    date_str = datetime.strptime(operation.get('date', ''), "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
    masked_card_number = f"{' '.join([operation.get('from', '')[:4], 'XX**', '****', operation.get('from', '')[-4:]])}" if 'from' in operation else ''
    masked_account_number = f"**{operation.get('to', '')[-4:]}" if 'to' in operation else ''

    amount = operation['operationAmount'].get('amount', '')
    currency = operation['operationAmount']['currency'].get('name', '')
    result = f"{date_str} {operation.get('description', '')}\n{masked_card_number} -> {masked_account_number}\n{operation.get('operationAmount', {}).get('amount', '')} {operation.get('operationAmount', {}).get('currency', {}).get('name', '')}\n"
    return result