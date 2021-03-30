import json
from datetime import datetime, date
from pprint import pprint

__all__ = ['DatetimeJSONEncoder', 'from_str_to_datetime_hook',]
d = '%d/%m/%Y'
dt = d + ' ' + '%H:%M:%S'

# класс, который преобразует объекты date и datetime в json объекты string
# при использовании методов dump и dumps, класс передается туда
# как именованный аргумент cls=DatetimeJSONEncoder
class DatetimeJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return {
                'value': o.strftime(dt),
                '__datetime__': True,
            }
        elif isinstance(o, date):
            return {
                'value': o.strftime(d),
                '__date__': True,
            }
        super().default(o)


# функция, которая будет использоваться в каестве хука при
# преобразовании json данных в объекты python
# при использовании методов loads() и load() передается
# туда как именованный аргумент object_hook=from_str_to_datetime_hook
# hook - это такой дополнительный фильтр, через которые прохоят данные

def from_str_to_datetime_hook(dct):
    print(dct, 1)
    if '__datetime__' in dct:
        return datetime.strptime(dct['value'], dt)
    elif '__date__' in dct:
        return datetime.strptime(dct['value'], d).date()
    return dct


# По всей видимости JSONEncoder для dump(s)
#                   JSONDecoder для load(s)


"""----------------------------- EXAMPLES --------------------------------------------"""
# Дальше идут примеры для использования DatetimeJSONEncoder и from_str_to_datetime_hook


if __name__ == '__main__':
    # ------ потенциальный объект для примера
    data = {
        'first_name': 'Eugene',
        'last_name': 'Petrov',
        'birthday': date(year=1986, month=9, day=29),
        'hired_at': datetime(2006, 9, 29, 12, 30, 5),
        'hobbies': [
            'guitar',
            'cars',
            'mountains',
            'adventures'
        ]
    }
    # pprint(data)
    # -----------------------------------------------



    """dump и dumps (DatetimeJSONEncoder)"""
    # -------------------------------------------------------
    # пример использования dumps
    json_data = json.dumps(data, cls=DatetimeJSONEncoder, indent=3)
    # pprint(json_data)

    # # пример использования dump
    # with open('../files/record_data.json', 'w', encoding='utf-8') as f:
        # json.dump(data, f, cls=DatetimeJSONEncoder, indent=3)
    # -------------------------------------------------------


    """load и loads (from_str_to_datetime_hook)"""
    # -------------------------------------------------------
    # # пример использования loads
    py_date = json.loads(json_data, object_hook=from_str_to_datetime_hook)
    pprint(py_date)

    # # пример использования load
    # with open('../files/record_data.json', 'r', encoding='utf-8') as f:
    #     file_py_date = json.load(f, object_hook=from_str_to_datetime_hook)
    #     pprint(file_py_date)
    # # -------------------------------------------------------