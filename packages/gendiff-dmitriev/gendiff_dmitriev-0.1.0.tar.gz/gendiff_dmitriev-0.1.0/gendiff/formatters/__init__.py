from .plain import make_plain
from .stylish import make_stylish
from .json import make_json


def get_formatter(name_format):
    """Returns the formatter"""
    if name_format == 'plain':
        return make_plain
    elif name_format == 'json':
        return make_json
    return make_stylish
