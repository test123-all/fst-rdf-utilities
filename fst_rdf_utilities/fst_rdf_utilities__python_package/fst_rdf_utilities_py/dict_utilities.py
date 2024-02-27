import re
from pathlib import Path
from copy import deepcopy
import sys
# sys.setrecursionlimit(5000)

import rdflib
from rdflib import URIRef
import requests
from bs4 import BeautifulSoup
import validators.url
from scipy import io as sio
import arrow


def combine_dicts_recursively(dict_1: dict, dict_2: dict) -> dict:
    def _combine_nested_dicts(d1, d2):
        sub_result_dict = {}
        for key in d1.keys():
            if key in d2.keys():
                if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                    sub_result_dict[key] = _combine_nested_dicts(d1[key], d2[key])
                elif d1[key] == d2[key]:
                    sub_result_dict[key] = d1[key]
                else:
                    raise ValueError(
                        f"You are trying to combine two dictionaries with the same key '{key}', but the values differ: {d1[key]} and {d2[key]}")
            else:
                sub_result_dict[key] = d1[key]


        for key, value in d2.items():
            if key not in sub_result_dict:
                sub_result_dict[key] = value

        return sub_result_dict


    result_dict = {}

    for key, value in dict_1.items():
        if key in dict_2:
            if isinstance(value, dict) and isinstance(dict_2[key], dict):
                result_dict[key] = _combine_nested_dicts(value, dict_2[key])
            elif value == dict_2[key]:
                result_dict[key] = value
            else:
                raise ValueError(
                    f"You are trying to combine two dictionaries with the same key '{key}', but the values differ: {value} and {dict_2[key]}")
        else:
            result_dict[key] = value

    for key, value in dict_2.items():
        if key not in result_dict:
            result_dict[key] = value

    return result_dict


def set_value_inside_nested_dict_with_path(input_struct: dict, struct_path: str, value):
    # Example: input_dict, 'a.b.c', 100

    # Validate the struct path (you can add your validation logic here)

    # Split the struct path
    splitted_struct_path = struct_path.split('.')

    # Traverse the nested structure
    # WARNING: This only works because python doesn't deep copy the dict contents, therefore current_struct still points
    # to the substructk of input struct. If the value gets changed in current_struct the variables get changed in
    # both structs!
    # If you don't want this you need to use the python standard library deepcopy module.
    # Please have a look at:
    # https://docs.python.org/3/library/copy.html
    if struct_path == '':
        input_struct = value
        return input_struct


    current_struct = input_struct
    for field in splitted_struct_path[:-1]:
        current_struct = current_struct[field]

    # Assign the value
    current_struct[splitted_struct_path[-1]] = value

    return input_struct


def get_value_inside_nested_dict_with_path(input_struct: dict, struct_path: str):
    # Example: input_dict, 'a.b.c', 100

    # Validate the struct path (you can add your validation logic here)

    # Split the struct path
    splitted_struct_path = struct_path.split('.')

    # Traverse the nested structure
    # WARNING: This only works because python doesn't deep copy the dict contents, therefore current_struct still points
    # to the substructk of input struct. If the value gets changed in current_struct the variables get changed in
    # both structs!
    # If you don't want this you need to use the python standard library deepcopy module.
    # Please have a look at:
    # https://docs.python.org/3/library/copy.html
    if struct_path == '':
        # TODO: Find better exception
        raise Exception("There was a empty dict_path '' provided!")

    current_struct = input_struct
    for field in splitted_struct_path[:-1]:
        current_struct = current_struct[field]

    value = current_struct[splitted_struct_path[-1]]

    return value