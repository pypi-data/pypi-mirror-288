import itertools


INDENT = 4
SHIFT_LEFT = 2
DEPTH_STEP = 1


def make_stylish(value, replacer=' ', spaces_count=4):
    """Formatter function. Describes changes to each key.
    Returns a string.
    """
    def iter_(current_value, depth):

        deep_indent_size = depth * spaces_count
        left_shift = replacer * (deep_indent_size - 2)
        current_indent = ((spaces_count * depth) - spaces_count) * replacer
        lines = []

        if isinstance(current_value, list):
            for i in current_value:
                if i['type'] == 'nested':
                    lines.append(f"{left_shift}  {i['key']}: {iter_(i['value'], depth + DEPTH_STEP)}") # noqa:501
                elif i['type'] == 'added':
                    lines.append(f"{left_shift}+ {i['key']}: {to_str(i['value'], depth + DEPTH_STEP)}") # noqa:501
                elif i['type'] == 'removed':
                    lines.append(f"{left_shift}- {i['key']}: {to_str(i['value'], depth + DEPTH_STEP)}") # noqa:501
                elif i['type'] == 'equal':
                    lines.append(f"{left_shift}  {i['key']}: {to_str(i['value'], depth + DEPTH_STEP)}") # noqa:501
                elif i['type'] == 'updated':
                        lines.append(f"{left_shift}- {i['key']}: {to_str(i['value1'], depth + DEPTH_STEP)}") # noqa:501
                        lines.append(f"{left_shift}+ {i['key']}: {to_str(i['value2'], depth + DEPTH_STEP)}") # noqa:501
        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return iter_(value, DEPTH_STEP)


def to_str(value, depth=0, replacer=' ', spaces_count=4):
    """Converts a value of different types to the required format"""
    deep_indent_size = depth * spaces_count
    deep_indent = replacer * deep_indent_size
    current_indent = ((spaces_count * depth) - spaces_count) * replacer
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            if isinstance(v, dict):
                lines.append(f"{deep_indent}{k}: {to_str(v, depth + DEPTH_STEP)}") # noqa:501
            else:
                lines.append(f"{deep_indent}{k}: {to_str(v)}")
        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)
    elif value is True or value is False:
        return str(value).lower()
    elif value is None:
        return 'null'
    return str(value)
