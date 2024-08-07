import pytest

import os

from gendiff.generate_diff import generate_diff


def get_fixture_path(file_name):
    """Returns the full path of the fixture."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path):
    """Reads the file."""
    with open(file_path, 'r') as f:
        result = f.read()
    return result


@pytest.mark.parametrize("file_name1, file_name2, formatter, expected_result", [
    ["file1.json", "file2.json", "stylish", "plain.txt"],
    ["file1.yaml", "file2.yml", "stylish", "plain.txt"],
    ["file1.json", "file2.yml", "stylish", "plain.txt"],
    ["file1_nested.json", "file2_nested.json", "stylish", "nested.txt"],
    ["file1_nested.yml", "file2_nested.yaml", "stylish", "nested.txt"],
    ["file1_nested.yml", "file2_nested.json", "stylish", "nested.txt"],
    ["file1_nested.json", "file2_nested.json", "plain", "flat_format.txt"],
    ["file1_nested.yml", "file2_nested.yaml", "plain", "flat_format.txt"],
    ["file1_nested.yml", "file2_nested.json", "plain", "flat_format.txt"],
    ["file1_nested.yml", "file2_nested.json", "json", "file_json.txt"],
    ["file1_nested.json", "file2_nested.json", "json", "file_json.txt"],
    ["file1_nested.yml", "file2_nested.yaml", "json", "file_json.txt"],
])
def test_generate_diff(file_name1, file_name2, formatter, expected_result):
    """Tests the operation of the function generate_diff.
    Accepts different file paths and formatters"""
    with open(get_fixture_path(expected_result)) as file:
        assert generate_diff(
            get_fixture_path(file_name1),
            get_fixture_path(file_name2),
            formatter
        ) == file.read()


def test_wrong_format():
    """Tests for unsupported format error."""
    with pytest.raises(ValueError) as e:
        generate_diff(
            get_fixture_path("file1_nested.json"),
            get_fixture_path("file.txt"),
        )

    assert str(e.value) == 'unsupported file format'
