from functools import reduce
import re

def luhn(code: str) -> bool:
    """
    Проверка корректности IMEI с использованием алгоритма Луна
    """
    LOOKUP = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
    code = reduce(str.__add__, filter(str.isdigit, code))
    evens = sum(int(i) for i in code[-1::-2])
    odds = sum(LOOKUP[int(i)] for i in code[-2::-2])
    return ((evens + odds) % 10 == 0)

def validate_imei(imei: str) -> bool:
    """
    Проверка формата IMEI
    """
    if not re.match(r'^\d{15}$', imei):
        return False
    return luhn(imei)

def format_response(data: dict, imei: str) -> str:
    """
    Форматирование информации об IMEI
    """
    str_data = f"Информация об IMEI {imei}\n\n"
    for k,v in data.items():
        if isinstance(v, dict):
            row = f"{k}:\n"
            for key, value in v.items():
                row += f"     {key}: {value}\n"
            str_data += row
        else:
            str_data += f"{k}: {v} \n"
    return str_data
