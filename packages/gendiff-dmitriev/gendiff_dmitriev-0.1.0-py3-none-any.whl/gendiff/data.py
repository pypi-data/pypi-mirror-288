import json
import yaml


def get_data(filepath):
    """Returns data from a file."""
    if get_format_file(filepath) == 'yaml':
        file_data = yaml.safe_load(open(filepath).read())
    else:
        file_data = json.load(open(filepath))
    return file_data


def get_format_file(filepath):
    """Returns the file format."""
    if filepath.endswith('.yaml'):
        return 'yaml'
    elif filepath.endswith('.yml'):
        return 'yaml'
    elif filepath.endswith('.json'):
        return 'json'
    else:
        raise ValueError('unsupported file format')
