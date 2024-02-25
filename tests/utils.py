from datetime import date
import pytest
from datetime import datetime, timedelta

DATA_AMOUNT = 21
PAGINATION_SIZE = 20
CREATED_ID = DATA_AMOUNT + 1


def generate_data_with_nums(data: dict, nums: int):
    modified_data_list = []
    for num in range(nums):
        modified_data = {}
        for key, value in data.items():
            if isinstance(value, date):
                new_value = value
            elif isinstance(value, str):
                new_value = f'{value}{num}'
            elif isinstance(value, int):
                new_value = value + num
            else:
                new_value = value
            modified_data[key] = new_value
        modified_data_list.append(modified_data)
    return modified_data_list


def get_time_now():
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')
    time = pytest.approx(current_time, abs=timedelta(seconds=1))
    return time


def datetimes_without_misecs(passed_value, current_value):
    passed_withot_misecs = str(passed_value)[:16]
    current_withot_misecs = str(current_value)[:16]
    return passed_withot_misecs, current_withot_misecs


def datetimes_compare(response: dict, start_at_2: str):
    start_at_1 = response.pop('start_at')
    start_at_res, start_at_exp = datetimes_without_misecs(
        start_at_1, start_at_2
    )

    assert start_at_res == start_at_exp
    return response


def object_without_field(obj, field_name):
    if field_name in obj:
        del obj[field_name]
    return obj


def expected_error_response(obj, field_name):
    return {
        'detail': [{
            'type': 'missing',
            'loc': ['body', field_name],
            'msg': 'Field required',
            'input': object_without_field(obj, field_name),
            'url': 'https://errors.pydantic.dev/2.6/v/missing'}]
    }
