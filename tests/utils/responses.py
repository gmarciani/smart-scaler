from json import loads as to_json


def match_status(rv, expected_code):
    """
    Test whether the HTTP status code of the return value matches the expected status code.
    :param rv: the return value.
    :param expected_code: the expected status code.
    :return: True, in case of a code match; False, otherwise.
    """
    actual_code = rv.status_code
    match_condition = actual_code == expected_code
    return match_condition


def match_data(rv, expected_data):
    """
    Test whether the JSON data of the return value matches the expected data.
    :param rv: the return value.
    :param expected_data: the expected data
    :return: True, in case of a data match; False, otherwise.
    """
    actual_data = dict(get_json(rv))
    match_condition = all(item in actual_data.items() for item in expected_data.items())
    return match_condition


def get_json(rv):
    """
    Retrieve the JSON data from the return values.
    :param rv: the return value.
    :return: (dict) the JSON data.
    """
    return to_json(rv.get_data(as_text=True))


def get_data_field(rv, field):
    """
    Retrieve the JSON data from the return values.
    :param rv: the return value.
    :param field: the field name.
    :return: (dict) the field value.
    """
    return get_json(rv)[field]