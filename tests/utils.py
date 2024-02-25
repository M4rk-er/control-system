from datetime import date, datetime, timedelta
from fastapi import status

import pytest


PAGINATION_SIZE = 20

SHIFT_DATA_AMOUNT = 21
SHIFT_ID = SHIFT_DATA_AMOUNT + 1

PRODUCT_DATA_AMOUNT = 7
PRODUCT_ID = PRODUCT_DATA_AMOUNT + 1


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


def get_aggregate_errors_params() -> list:
    return [
        (
            {'sku': 'unexistssku', 'shift_id': 456},
            status.HTTP_404_NOT_FOUND,
            {'detail': 'There are no Product.'},
        ),
        (
            {'sku': 'skuintest', 'shift_id': 999},
            status.HTTP_404_NOT_FOUND,
            {'detail': 'There are no ShiftTask.'},
        ),
        (
            {'sku': 'skuintest', 'shift_id': 1},
            status.HTTP_400_BAD_REQUEST,
            {'detail': f'unique code already used ', },
        ),
        (
            {'sku': 'skuintest', 'shift_id': 2},
            status.HTTP_400_BAD_REQUEST,
            {'detail': 'unique code is attached to another batch'},
        ),
    ]


def get_invalid_product_params() -> list:
    return [
        (
            [{'sku': 'testsku', 'batch_number': 987, 'batch_date': str(date(2000, 1, 1))}],
            status.HTTP_201_CREATED,
            [],
        ),
        (
            [{'sku': 'unexisted', 'batch_number': 123, 'batch_date': str(date(2024, 1, 1))}],
            status.HTTP_201_CREATED,
            [],
        ),
    ]
