import unittest
from pathlib import Path

import numpy as np
import rdflib
import scipy.io as sio

from fst_rdf_utilities__python_package.fst_rdf_utilities_py import utilities
from fst_rdf_utilities__python_package.fst_rdf_utilities_py import dict_utilities


# TODO: FIXME: The the following test case is a script, that was used to develop the package.
#  The example struct can be used to write a test to load a mat file and to test if the behaviour of the scipy package
#  somehow changed.
# class TestUtil(unittest.TestCase):
#     def test_script(self) -> None:
#         test_dict = {
#             'UUID': '0184ebd9-988b-7bba-8203-06be5cf6bbb8',
#             'identification_string': 'D092',
#             'measurement_range': {
#                 'from': 0,
#                 'to': 10,
#                 'unit': 'bar'
#             },
#             'output_range': {
#                 'from': 0,
#                 'to': 10,
#                 'unit': 'V'
#             },
#             'characteristic_line': {
#                 'slope': 1,
#                 'offset': 0
#
#         data_tuple = ('0184ebd9-988b-7bba-8203-06be5cf6bbb8',
#                       'D092',
#                       measurement_range_structured_numpy_array,
#                       output_range_structured_numpy_array,
#                       characteristic_line_structured_numpy_array,
#                       'Piezoresistiv',
#                       'Keller',
#                       'PAA-33X/10bar',
#                       '1011246')
#
#         x = np.array([data_tuple], dtype=[('UUID', '<U36'),
#                                                 ('identification_string', '<U4'),
#                                                 ('measurement_range', 'void'),
#                                                 ('output_range', 'void'),
#                                                 ('characteristic_line', 'void'),
#                                                 ('measurement_principle', '<U13'),
#                                                 ('manufacturer', '<U6'),
#                                                 ('product_label', '<U13'),
#                                                 ('serial_number', '<U7')
#                                           ])

class Testload_sensor_rdf_and_parse_to_dict(unittest.TestCase):
    def test_00(self) -> None:
        test_dict = {
            'UUID': 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8',
            'identification_string': 'fst-inv:D092',
            'measurement_range': {
                'from': 0.0,
                'to': 10.0,
                'unit': 'bar'
            },
            # 'output_range': {
            #     'from': 0,
            #     'to': 10,
            #     'unit': 'V'
            # },
            'characteristic_line': {
                'slope': 1.0,
                'offset': 0.0

            },
            'measurement_principle': 'Piezoresistiv',
            'manufacturer': 'Keller',
            'product_label': 'PAA-33X/10bar',
            'serial_number': '1011246'
        }
        [sensor_dict, _] = utilities.load_sensor_rdf_and_parse_to_dict(
            'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8')
        self.assertEqual(sensor_dict, test_dict)


class Testparse_url_into_parts(unittest.TestCase):
    def test_00(self) -> None:
        url = 'https://git.rwth-aachen.de/fst-tuda/public/metadata/fst_measurement_equipment/-/tree/main/0184ebd9-988b-7bb9-aa19-1b8573bd0a50/rdf.ttl'

        anticipated_repository_url_variable_dict = {
            'base_url': 'https://git.rwth-aachen.de',
            'project_path_url': 'fst-tuda/public/metadata/fst_measurement_equipment',
            'repository_file_path': '0184ebd9-988b-7bb9-aa19-1b8573bd0a50/rdf.ttl'
        }

        repository_url_variable_dict = utilities.parse_url_into_parts(url)
        self.assertEqual(anticipated_repository_url_variable_dict, repository_url_variable_dict)


