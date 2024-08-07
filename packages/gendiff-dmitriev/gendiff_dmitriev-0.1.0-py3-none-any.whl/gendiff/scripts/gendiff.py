#!/usr/bin/env python3
from gendiff.parser import parse
from gendiff.generate_diff import generate_diff


def main():
    print(generate_diff(*parse()))


if __name__ == '__main__':
    main()
