import unittest
from pathlib import Path

import numpy as np
import rdflib
import scipy.io as sio

from rdf_test import utilities
from rdf_test import dict_utilities


class TestUti(unittest.TestCase):
    def test_script(self) -> None:
        test_dict = {
            'UUID': '0184ebd9-988b-7bba-8203-06be5cf6bbb8',
            'identification_string': 'D092',
            'measurement_range': {
                'from': 0,
                'to': 10,
                'unit': 'bar'
            },
            'output_range': {
                'from': 0,
                'to': 10,
                'unit': 'V'
            },
            'characteristic_line': {
                'slope': 1,
                'offset': 0

            },
            'measurement_principle': 'Piezoresistiv',
            'manufacturer': 'Keller',
            'product_label': 'PAA-33X/10bar',
            'serial_number': '1011246'
        }

        mat_file_path = Path('./example_mat_struct.mat')
        mat_struct = sio.loadmat(str(mat_file_path.resolve()))

        test_dict2 = {'ID_0184ebd9_988b_7bba_8203_06be5cf6bbb8': test_dict}
        # self.assertEqual(mat_struct['example_mat_struct'], x)
        sio.savemat('test2.mat', test_dict2)


# Wenn ich es schaffe das dan structured numpy array zu erstellen und das gleich dem geladenen ist müsste das gespeicherte gleich dem in matlab sein. D.h. ich kann dann beliebig daten zwischen python und matlab austauschen


# # TODO: Everything is hardcoded, the job can be done recursevily and automatically
#         measurement_range_structured_numpy_array = np.array([(0, 10, 'bar')], dtype=[('from', 'i4'), ('to', 'i4'), ('unit', '<U3')])
#         output_range_structured_numpy_array = np.array([(0, 10, 'V')], dtype=[('from', 'i4'), ('to', 'i4'), ('unit', '<U1')])
#         characteristic_line_structured_numpy_array = np.array([(1, 0)], dtype=[('slope', 'i4'), ('offset', 'i4')])
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


class Testget_version_commit_hash(unittest.TestCase):
    def test_00(self) -> None:
        url = 'https://git.rwth-aachen.de/fst-tuda/public/metadata/fst_measurement_equipment/-/tree/main/0184ebd9-988b-7bb9-aa19-1b8573bd0a50/rdf.ttl'
        version_commit_hash = utilities.get_version_commit_hash(url)
        anticipated_version_commit_hash = '88249e227d1011759cf91be3c131afdb4cb67047'

        self.assertEqual(anticipated_version_commit_hash, version_commit_hash)


class Testsave_sensor_rdf_as_mat_file(unittest.TestCase):
    def test_00(self) -> None:
        pID_url = 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8'
        utilities.save_sensor_rdf_as_mat_file(pID_url, './')