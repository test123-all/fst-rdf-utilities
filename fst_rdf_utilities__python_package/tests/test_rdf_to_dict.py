import unittest
from pathlib import Path

# import numpy as np
import rdflib
# import scipy.io as sio

from fst_rdf_utilities_py import utilities
from fst_rdf_utilities_py import rdf_to_dict

persistent_id_url = 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8'

expected_dict = {}
expected_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8'] = \
    {'prefix': 'https://w3id.org/fst/resource/',
     'type': {
         'prefix': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
         'PhysicalObject': {
             'prefix': 'http://purl.org/dc/dcmitype/',
         },
         'Sensor': {
             'prefix': 'http://www.w3.org/ns/sosa/',
         },
     },
     'maintainedBy': {
         'prefix': 'http://dbpedia.org/ontology/',
         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
         'literal': 'Rexer',
     },
     'owner': {
         'prefix': 'http://dbpedia.org/ontology/',
         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
         'literal': 'FST',

     },
     'identifier': {
         'prefix': 'http://purl.org/dc/terms/',
         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
         'literal': [
             '0184ebd9-988b-7bba-8203-06be5cf6bbb8',
             'fst-inv:D092'],
     },
     'modified': {
         'prefix': 'http://purl.org/dc/terms/',
         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
         'literal': 'None',
     },
     'documentation': {
         'prefix': 'http://schema.org/',
         'docs': {
             'prefix': 'https://w3id.org/fst/resource/',
         },
     },
     'keywords': {
         'prefix': 'http://schema.org/',
         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
         'literal': ['Druck', 'Piezoresistiv', 'absolut'],
     },
     'location': {
         'prefix': 'http://schema.org/',
         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
         'literal': 'Hydropulser Schrank',
     },
     'manufacturer': {
         'prefix': 'http://schema.org/',
         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
         'literal': 'Keller',
     },
     'name': {
         'prefix': 'http://schema.org/',
         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
         'literal': 'PAA-33X/10bar',
     },
     'serialNumber': {
         'prefix': 'http://schema.org/',
         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
         'literal': '1011246',
     },
     'subjectOf': {
         'prefix': 'http://schema.org/',
         'docs': {
             'prefix': 'https://w3id.org/fst/resource/',
         },
     },
     'usedProcedure': {
         'prefix': 'http://www.w3.org/ns/sosa/',
         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
         'literal': 'Piezoresistiv',
     },
     'hasSystemCapability': {
         'prefix': 'http://www.w3.org/ns/ssn/systems/',
         'SensorCapability': {
             'prefix': 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/',
             'type': {
                 'prefix': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                 'Property': {
                     'prefix': 'http://www.w3.org/ns/ssn/',
                 },
                 'SystemCapability': {
                     'prefix': 'http://www.w3.org/ns/ssn/systems/',
                 },
             },
             'name': {
                 'prefix': 'http://schema.org/',
                 'datatype': 'http://www.w3.org/2001/XMLSchema#string',
                 'literal': 'sensor capabilities',
             },
             'comment': {
                 'prefix': 'http://www.w3.org/2000/01/rdf-schema#',
                 'datatype': 'http://www.w3.org/2001/XMLSchema#string',
                 'literal': 'sensor capabilities not regarding any conditions at this time'
             },
             'hasProperty': {
                 # -> das ist scheiße wegen der liste evtl muss ich das so weiter machen und die sachen die aus / bestehen nochmal seperat in das struct laden
                 'prefix': 'http://www.w3.org/ns/ssn/',
                 'Bias': {
                     'prefix': 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/',
                     'type': {
                         'prefix': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                         'Property': {
                             'prefix': 'http://www.w3.org/ns/ssn/',
                         },
                         'SystemProperty': {
                             'prefix': 'http://www.w3.org/ns/ssn/systems/',
                         },
                     },
                     'name': {
                         'prefix': 'http://schema.org/',
                         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
                         'literal': 'bias',
                     },
                     'value': {
                         'prefix': 'http://schema.org/',
                         'literal': 0.0,
                         'datatype': 'http://www.w3.org/2001/XMLSchema#double',
                     },
                     'comment': {
                         'prefix': 'http://www.w3.org/2000/01/rdf-schema#',
                         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
                         'literal': 'offset',
                     },
                     'isPropertyOf': {
                         'prefix': 'http://www.w3.org/ns/ssn/',
                         'SensorCapability': {
                             'prefix': 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/',
                         },
                     },
                 },
                 'MeasurementRange': {
                     'prefix': 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/',
                     'type': {
                         'prefix': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                         'Quantity': {
                             'prefix': 'http://qudt.org/schema/qudt/',
                         },
                         'Property': {
                             'prefix': 'http://www.w3.org/ns/ssn/',
                         },
                         'MeasurementRange': {
                             'prefix': 'http://www.w3.org/ns/ssn/systems/',
                         },
                     },
                     'hasQuantityKind': {
                         'prefix': 'http://qudt.org/schema/qudt/',
                         'Pressure': {
                             'prefix': 'http://qudt.org/vocab/quantitykind/',
                         },
                     },
                     'unit': {
                         'prefix': 'http://qudt.org/schema/qudt/',
                         'BAR': {
                             'prefix': 'http://qudt.org/vocab/unit/',
                         },
                     },
                     'maxValue': {
                         'prefix': 'http://schema.org/',
                         'literal': 10,
                         'datatype': 'http://www.w3.org/2001/XMLSchema#integer',
                     },
                     'minValue': {
                         'prefix': 'http://schema.org/',
                         'literal': 0,
                         'datatype': 'http://www.w3.org/2001/XMLSchema#integer',
                     },
                     'name': {
                         'prefix': 'http://schema.org/',
                         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
                         'literal': 'measurement range',
                     },
                     'valueReference': {
                         'prefix': 'http://schema.org/',
                         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
                         'literal': 'absolut',
                     },
                     'isPropertyOf': {
                         'prefix': 'http://www.w3.org/ns/ssn/',
                         'SensorCapability': {
                             'prefix': 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/',
                         },
                     },
                 },
                 'Sensitivity': {
                     'prefix': 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/',
                     'type': {
                         'prefix': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                         'Property': {
                             'prefix': 'http://www.w3.org/ns/ssn/',
                         },
                         'Sensitivity': {
                             'prefix': 'http://www.w3.org/ns/ssn/systems/',
                         },
                     },
                     'name': {
                         'prefix': 'http://schema.org/',
                         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
                         'literal': 'sensitivity',
                     },
                     'value': {
                         'prefix': 'http://schema.org/',
                         'literal': 1.0,
                         'datatype': 'http://www.w3.org/2001/XMLSchema#double',
                     },
                     'comment': {
                         'prefix': 'http://www.w3.org/2000/01/rdf-schema#',
                         'literal': 'gain',
                         'datatype': 'http://www.w3.org/2001/XMLSchema#string',
                     },
                     'isPropertyOf': {
                         'prefix': 'http://www.w3.org/ns/ssn/',
                         'SensorCapability': {
                             'prefix': 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/',
                         },
                     },
                 },
             },
         },
     }
     }

class Test_small_parse_example(unittest.TestCase):
    def test_00(self) -> None:
        expected_small_parse_example_dict = {}
        expected_small_parse_example_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8'] = \
            {'prefix': 'https://w3id.org/fst/resource/',
             'type': {
                 'prefix': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                 'PhysicalObject': {
                     'prefix': 'http://purl.org/dc/dcmitype/',
                 },
                 'Sensor': {
                     'prefix': 'http://www.w3.org/ns/sosa/',
                 },
             },
             'maintainedBy': {
                 'prefix': 'http://dbpedia.org/ontology/',
                 'datatype': 'http://www.w3.org/2001/XMLSchema#string',
                 'literal': 'Rexer',
             },
             }

        subject = rdflib.URIRef('https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8')

        graph = rdflib.Graph()
        graph.add((rdflib.URIRef('https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8'),
                   rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                   rdflib.URIRef('http://purl.org/dc/dcmitype/PhysicalObject')))

        graph.add((rdflib.URIRef('https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8'),
                   rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                   rdflib.URIRef('http://www.w3.org/ns/sosa/Sensor')))

        graph.add((rdflib.URIRef('https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8'),
                   rdflib.URIRef('http://dbpedia.org/ontology/maintainedBy'),
                   rdflib.Literal('Rexer', datatype=rdflib.URIRef('http://www.w3.org/2001/XMLSchema#string'))))

        graph.bind(None, 'https://w3id.org/fst/resource/')
        graph.bind(None, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        graph.bind(None, 'http://purl.org/dc/dcmitype/')
        graph.bind(None, 'http://www.w3.org/ns/sosa/')
        graph.bind(None, 'http://dbpedia.org/ontology/')

        sub_dict = rdf_to_dict._parse_subgraph_to_dict(subgraph=graph, subject=subject)

        self.assertEqual(expected_small_parse_example_dict, sub_dict)


class Test_get_uuid_and_prefix(unittest.TestCase):
    # TODO: save the .ttl file on the file system
    graph, redirect_file_url_cleaned = utilities.load_git_rdf(persistent_id_url=persistent_id_url)
    namespaces = set(graph.namespaces())

    def test_00(self) -> None:
        uriref = rdflib.term.URIRef('https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/SensorCapability')
        prefix, uuid = rdf_to_dict._get_uuid_and_prefix(uriref, self.namespaces)

        self.assertEqual('https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/', prefix)
        self.assertEqual('SensorCapability', uuid)

    def test_01(self) -> None:
        uriref = rdflib.term.URIRef('http://www.w3.org/ns/ssn/systems/Sensitivity')
        prefix, uuid = rdf_to_dict._get_uuid_and_prefix(uriref, self.namespaces)

        self.assertEqual('http://www.w3.org/ns/ssn/systems/', prefix)
        self.assertEqual('Sensitivity', uuid)


class Test__parse_RDF_to_dict(unittest.TestCase):
    current_file_dir_path = Path(__file__).parent
    graph = rdflib.Graph(base=rdflib.URIRef('https://w3id.org/fst/resource/'))
    with Path(f'{current_file_dir_path}/sensor_rdf.ttl').open('r') as f:
        graph.parse(data=f.read(), format="turtle")

    parsed_dict = rdf_to_dict._parse_RDF_graph_to_dict(graph=graph, main_subject=rdflib.URIRef(
        persistent_id_url))  # 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8'

    def test_00(self) -> None:
        # Full test
        self.maxDiff = None
        self.assertEqual(expected_dict, self.parsed_dict)
