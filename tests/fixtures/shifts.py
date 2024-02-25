from datetime import date

import pytest

from tests.utils import (expected_error_response,
                         get_time_now,
                         object_without_field,
                         SHIFT_ID)


@pytest.fixture
def shift_body() -> dict:
    shift = {
        'ПредставлениеЗаданияНаСмену': 'ЗаданиеТест',
        'Смена': 'СменаТест',
        'РабочийЦентр': 'ЦентрТест',
        'Бригада': 'БригадаТест',
        'НомерПартии': 123,
        'ДатаПартии': '2024-01-01',
        'Номенклатура': 'НоменклатураТест',
        'КодЕКН': 'КодЕКНТест',
        'ИдентификаторРЦ': 'ИдентификаторРЦТест',
    }
    return shift


@pytest.fixture
def updated_shift_request() -> dict:
    shift = {
        'ПредставлениеЗаданияНаСмену': 'ЗаданиеТестОбновление',
        'Смена': 'СменаТесОбновлениет',
        'РабочийЦентр': 'ЦентрТестОбновление',
        'Бригада': 'БригадаТесОбновлениет',
        'НомерПартии': 123,
        'ДатаПартии': '2024-01-01',
        'Номенклатура': 'НоменклатураТестОбновление',
        'КодЕКН': 'КодЕКНТестОбновление',
        'ИдентификаторРЦ': 'ИдентификаторРЦТестОбновление',
    }
    return shift


@pytest.fixture
def updated_shift_response() -> dict:
    shift = {
        'id': SHIFT_ID,
        'task': 'ЗаданиеТестОбновление',
        'shift': 'СменаТесОбновлениет',
        'work_center': 'ЦентрТестОбновление',
        'brigade': 'БригадаТесОбновлениет',
        'batch_number': 123,
        'batch_date': '2024-01-01',
        'nomenclature': 'НоменклатураТестОбновление',
        'EKN_code': 'КодЕКНТестОбновление',
        'RC_identifier': 'ИдентификаторРЦТестОбновление',
        'is_closed': False,
        'start_at': get_time_now(),
        'closed_at': None,
    }
    return shift


@pytest.fixture
def shift_response() -> dict:
    shift = {
        'id': SHIFT_ID,
        'task': 'ЗаданиеТест',
        'shift': 'СменаТест',
        'work_center': 'ЦентрТест',
        'brigade': 'БригадаТест',
        'batch_number': 123,
        'batch_date': '2024-01-01',
        'nomenclature': 'НоменклатураТест',
        'EKN_code': 'КодЕКНТест',
        'RC_identifier': 'ИдентификаторРЦТест',
        'is_closed': False,
        'start_at': get_time_now(),
        'closed_at': None,
    }
    return shift


@pytest.fixture(scope='session')
def shift_db() -> dict:
    shift = {
        'task': 'ПредставлениеЗаданияНаСмену',
        'shift': 'Смена',
        'work_center': 'РабочийЦентр',
        'brigade': 'Бригада',
        'batch_number': 456,
        'batch_date': date(year=2024, month=1, day=1),
        'nomenclature': 'Номенклатура',
        'EKN_code': 'КодЕКН',
        'RC_identifier': 'ИдентификаторРЦ',
    }
    return shift


SHIFT_REQUIRED_FIELDS = [
    'ПредставлениеЗаданияНаСмену',
    'Смена',
    'РабочийЦентр',
    'Бригада',
    'НомерПартии',
    'ДатаПартии',
    'Номенклатура',
    'КодЕКН',
    'ИдентификаторРЦ',
]


@pytest.fixture(params=SHIFT_REQUIRED_FIELDS)
def shift_without_value(shift_body, request):
    field_name = request.param
    shift = object_without_field(shift_body, field_name=field_name)
    response = expected_error_response(shift_body, field_name=field_name)
    return shift, response
