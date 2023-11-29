import json
from datetime import datetime
import os


def read_operations_from_json(file_path):
    with open(file_path, 'r', encoding='Utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []  # Возвращаем пустой список в случае ошибки декодирования JSON
    return data


def format_operation(operation):
    if 'date' not in operation or 'operationAmount' not in operation:
        return "Недействительная операция"

    date_str = datetime.strptime(operation.get('date', ''), "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
    card_data = operation.get("from", "").split(" ")
    card_name = " ".join(card_data[:-1])
    card_number = card_data[-1]

    if "from" not in operation:
        masked_card_number = "Номер счета неизвестен"
    else:
        masked_card_number = (f"{card_name} " + f"{' '.join([card_number[:4], card_number[4:6] + '**', '****', card_number[-4:]])}")

    masked_account_number = f"Счет **{operation.get('to', '')[-4:]}"

    amount = operation['operationAmount'].get('amount', '')
    currency = operation['operationAmount']['currency'].get('name', '')
    result = (
        f"{date_str} {operation.get('description', '')}\n"
        f"{masked_card_number} -> {masked_account_number}\n"
        f"{amount} {currency}\n"
    )
    return result


def display_last_operations(operations):
    if not operations:
        print("Операции не найдены.")
        return

    last_operations = sorted(operations, key=lambda x: datetime.strptime(x['date'],"%Y-%m-%dT%H:%M:%S.%f") if 'date' in x else datetime.min, reverse=True)[:5]
    formatted_operations = [format_operation(operation) for operation in last_operations]
    result = "\n\n".join(formatted_operations)
    print(result)


if __name__ == "__main__":
    # Используем относительный путь для файла JSON
    file_path = os.path.join(os.path.dirname(__file__), "..", "operations.json")
    operations = read_operations_from_json(file_path)
    display_last_operations(operations)
