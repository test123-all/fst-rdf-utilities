import unittest

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
#             },
#             'measurement_principle': 'Piezoresistiv',
#             'manufacturer': 'Keller',
#             'product_label': 'PAA-33X/10bar',
#             'serial_number': '1011246'
#         }
#
#         mat_file_path = Path('./example_mat_struct.mat')
#         mat_struct = sio.loadmat(str(mat_file_path.resolve()))
#
#         test_dict2 = {'ID_0184ebd9_988b_7bba_8203_06be5cf6bbb8': test_dict}
#         # self.assertEqual(mat_struct['example_mat_struct'], x)
#         sio.savemat('test2.mat', test_dict2)

# TODO: Theoretically this can be used to create a structure numpy array per hand and the same in matlab as mat to
#  better understand how the mat files get mapped to numpy.


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


