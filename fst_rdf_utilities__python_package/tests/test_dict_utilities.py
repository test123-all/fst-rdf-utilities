import unittest

from fst_rdf_utilities_py import dict_utilities

class Testcombine_dicts_recursively(unittest.TestCase):
    def test_00(self):
        dict_1 = {
            'a': 'test1',
            'b': {
                'b_c': 'test2',
                'b_d': 'te',
            }
        }

        dict_2 = {
            'b': {
                'b_e': 'gr',
            },
            'f': 'grgr',
        }

        expected_dict = {
            'a': 'test1',
            'b': {
                'b_c': 'test2',
                'b_d': 'te',
                'b_e': 'gr',
            },
            'f': 'grgr',
        }

        parsed_dict = dict_utilities.combine_dicts_recursively(dict_1, dict_2)
        dict_utilities.combine_dicts_recursively(expected_dict, parsed_dict)

    def test_01(self):
        # Test the combine_dicts_recursively function with deeper nesting.
        dict_1 = {
            'a': 'test1',
            'b': {
                'b_c': 'test2',
                'b_d': {
                    'b_d_e': 'nested1',
                    'b_d_f': 'nested2',
                },
            },
            'g': 'hello'
        }

        dict_2 = {
            'b': {
                'b_d': {
                    'b_d_e': 'nested1',
                    'b_d_h': 'nested3',
                },
                'b_i': 'nestedtest',
            },
            'j': 'testtst',
        }

        expected_dict = {
            'a': 'test1',
            'b': {
                'b_c': 'test2',
                'b_d': {
                    'b_d_e': 'nested1',
                    'b_d_f': 'nested2',
                    'b_d_h': 'nested3',
                },
                'b_i': 'nestedtest',
            'g': 'hello',
            'j': 'testtst',
            },
        }

        parsed_dict = dict_utilities.combine_dicts_recursively(dict_1, dict_2)
        dict_utilities.combine_dicts_recursively(expected_dict, parsed_dict)

    def test_02(self):
        # Test for the combine_dicts_recursively function that it correctly raises an exception.
        dict_1 = {
            'a': 'test1',
            'b': {
                'b_c': 'test2',
                'b_d': 'te',
            }
        }

        dict_2 = {
            'b': {
                'b_c': 'test2VERSCHIEDEN',
                'b_e': 'gr',
            },
            'f': 'grgr',
        }
        with self.assertRaises(ValueError):
            parsed_dict = dict_utilities.combine_dicts_recursively(dict_1, dict_2)

class Testset_value_inside_nested_dict_with_path(unittest.TestCase):
    def test_00(self):
        input_dict = {'a': {
                            'b': {
                                'c': 42,
                                'g': 20
                            },
                            'd': {
                                'e': 50
                            }
                            }
        }
        output_dict = dict_utilities.set_value_inside_nested_dict_with_path(input_dict, 'a.b.c', 100)

        expected_dict = input_dict
        expected_dict['a']['b']['c'] = 100
        self.assertEqual(expected_dict, output_dict)


class Testget_value_inside_nested_dict_with_path(unittest.TestCase):
    def test_00(self):
        input_dict = {'a': {
                            'b': {
                                'c': 42,
                                'g': 20,
                            },
                            'd': {
                                'e': 50
                            }
                            }
        }
        output_value = dict_utilities.get_value_inside_nested_dict_with_path(input_dict, 'a.d.e')

        expected_value = input_dict['a']['d']['e']

        self.assertEqual(expected_value, output_value)