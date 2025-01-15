
def load_sensor_rdf_and_parse_to_dict(persistent_id_url: str) -> [dict, str]:
    """
    # First example to load sensor data via RDF queries.

    """
    [g, redirect_file_url_cleaned] = load_git_rdf(persistent_id_url)

    # Get UUID, identification_string
    sparql_query = """
    PREFIX dcterms: <http://purl.org/dc/terms/>

    SELECT * WHERE {
    ?entity dcterms:identifier ?identifier .
    }
    """
    qres = g.query(sparql_query)

    identification_string = ''
    for row in qres:
        if 'fst-inv:' in row.identifier:
            identification_string = row.identifier

    # Get measurement_range
    sparql_query = """
    PREFIX schema: <http://schema.org/>
    PREFIX qudt: <http://qudt.org/schema/qudt/>
    SELECT * WHERE {
    ?entity schema:maxValue ?max_value;
            schema:minValue ?min_value;
            qudt:unit ?unit .
    }
    """
    qres = g.query(sparql_query)

    measurement_range_max_value = None
    measurement_range_min_value = None
    for row in qres:
        measurement_range_max_value = row.max_value
        measurement_range_min_value = row.min_value
        unit_ref = row.unit
        symbol_ref = URIRef('http://qudt.org/schema/qudt/symbol')
        if (None, symbol_ref, None) not in g:
            if validators.url(unit_ref):
                g_neu = rdflib.Graph()
                g_neu.parse(unit_ref)
                g = g + g_neu

    sparql_query = """
    PREFIX schema: <http://schema.org/>
    PREFIX qudt: <http://qudt.org/schema/qudt/>
    SELECT * WHERE {
    ?entity schema:maxValue ?max_value;
            schema:minValue ?min_value;
            qudt:unit ?unit .
    ?unit qudt:symbol ?symbol .
    }
    """
    qres = g.query(sparql_query)
    measurement_range_min_unit_symbol = None
    for row in qres:
        measurement_range_min_unit_symbol = row.symbol
    # TODO: FIXME need to get unit recursively
    # TODO: Kann ich mit der Bibliothek rekursiv suchen?

    # Get output_range
    # FIXME: TODO: isn't implemented inside the RDF!

    # Get characteristic_line
    sparql_query = """
        PREFIX schema: <http://schema.org/>

        SELECT * WHERE {
        ?entity schema:name "sensitivity" ;
                schema:value ?sensitivity_value .

        }
        """
    qres = g.query(sparql_query)

    characteristic_line_sensitivity = None
    for row in qres:
        characteristic_line_sensitivity = row.sensitivity_value

    sparql_query = """
    PREFIX schema: <http://schema.org/>

    SELECT * WHERE {
    ?entity schema:name "bias" ;
            schema:value ?offset_value .
    }
    """
    qres = g.query(sparql_query)

    characteristic_line_offset = None
    for row in qres:
        characteristic_line_offset = row.offset_value

    # Get manufacturer, product_label, serial_number
    sparql_query = """
    PREFIX schema: <http://schema.org/>

    SELECT * WHERE {
    ?entity schema:manufacturer ?manufacturer ;
            schema:name ?name ;
            schema:serialNumber ?serial_number .
    }
    """
    qres = g.query(sparql_query)

    manufacturer = None
    product_label = None
    serial_number = None

    for row in qres:
        manufacturer = row.manufacturer
        product_label = row.name
        serial_number = row.serial_number

    # Get measurement_principle
    sparql_query = """
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    SELECT * WHERE {
    ?entity sosa:usedProcedure ?procedure.
    }
    """
    qres = g.query(sparql_query)

    procedure = None
    for row in qres:
        procedure = row.procedure

    sensor_dict = {
                'p_ID': persistent_id_url, #evtl. zu PID ändern
                'identification_string': str(identification_string),
                'measurement_range': {
                    'from': float(measurement_range_min_value),
                    'to': float(measurement_range_max_value),
                    'unit': str(measurement_range_min_unit_symbol)
                },
                # 'output_range': {
                #     'from': 0,
                #     'to': 10,
                #     'unit': 'V'
                # },
                'characteristic_line': {
                    'slope': float(characteristic_line_sensitivity),
                    'offset': float(characteristic_line_offset)
                },
                'measurement_principle': str(procedure),
                'manufacturer': str(manufacturer),
                'product_label': str(product_label),
                'serial_number': str(serial_number),
                'type': 'Sensor'
            }

    return [sensor_dict, redirect_file_url_cleaned]

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


def save_sensor_rdf_as_mat_file(pID_url: str, save_to_directory_path: [Path, str]) -> None:
    [sensor_dict, redirect_file_url_cleaned] = load_sensor_rdf_and_parse_to_dict(pID_url)

    TTL = 1800  # seconds standard time dns cache time
    sensor_dict['UUID'] = {
        'URI': sensor_dict['UUID'],
        'version_commit_hash': get_version_commit_hash(redirect_file_url_cleaned),
        'dataset_record_metadata': {
            'data_cached_at_timestamp': str(arrow.utcnow()),
            'TTL': {
                'name': 'time to life',
                'value': TTL,
                'unit': 's'
            }
        }
    }

    # Turn pid into name
    # file_name = pID_url.replace('/', '_').replace('.', '_').replace(':', '_').replace('-', '_')
    UUID = pID_url.split("/")[-1]
    file_name = f'pID_{UUID.replace("-", "_")}'

    test_dict = {f'{file_name}': sensor_dict}
    # self.assertEqual(mat_struct['example_mat_struct'], x)
    sio.savemat(f'{save_to_directory_path}/{file_name}.mat', test_dict)

    # class Testget_predicates_for_current_subject(unittest.TestCase):
    #     graph, redirect_file_url_cleaned = utilities.load_git_rdf(persistent_id_url=persistent_id_url)
    #
    #     def test_00(self) -> None:
    #         current_subject = rdflib.term.URIRef('https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8')
    #
    #         expected_predicates_for_current_subject_list = [
    #             rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
    #             rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
    #             rdflib.term.URIRef('http://dbpedia.org/ontology/maintainedBy'),
    #             rdflib.term.URIRef('http://dbpedia.org/ontology/owner'),
    #             rdflib.term.URIRef('http://purl.org/dc/terms/identifier'),
    #             rdflib.term.URIRef('http://purl.org/dc/terms/identifier'),
    #             rdflib.term.URIRef('http://purl.org/dc/terms/modified'),
    #             rdflib.term.URIRef('http://schema.org/documentation'),
    #             rdflib.term.URIRef('http://schema.org/keywords'),
    #             rdflib.term.URIRef('http://schema.org/keywords'),
    #             rdflib.term.URIRef('http://schema.org/keywords'),
    #             rdflib.term.URIRef('http://schema.org/location'),
    #             rdflib.term.URIRef('http://schema.org/manufacturer'),
    #             rdflib.term.URIRef('http://schema.org/name'),
    #             rdflib.term.URIRef('http://schema.org/serialNumber'),
    #             rdflib.term.URIRef('http://schema.org/subjectOf'),
    #             rdflib.term.URIRef('http://www.w3.org/ns/sosa/usedProcedure'),
    #             rdflib.term.URIRef('http://www.w3.org/ns/ssn/systems/hasSystemCapability')]
    #
    #         expected_multiple_predicates_for_current_subject = {
    #             rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
    #             rdflib.term.URIRef('http://purl.org/dc/terms/identifier'),
    #             rdflib.term.URIRef('http://schema.org/keywords')}
    #
    #         (predicates_for_current_subject_list,
    #          multiple_predicates_for_current_subject) = rdf_to_dict.get_predicates_for_current_subject(current_subject,
    #                                                                                                    self.graph)
    #         self.assertEqual(expected_predicates_for_current_subject_list, predicates_for_current_subject_list)
    #         self.assertEqual(expected_multiple_predicates_for_current_subject, multiple_predicates_for_current_subject)
    #
    #     def test_01(self) -> None:
    #         current_subject = rdflib.term.URIRef(
    #             'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/MeasurementRange')
    #
    #         expected_predicates_for_current_subject_list = [
    #             rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
    #             rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
    #             rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
    #             rdflib.term.URIRef('http://qudt.org/schema/qudt/hasQuantityKind'),
    #             rdflib.term.URIRef('http://qudt.org/schema/qudt/unit'),
    #             rdflib.term.URIRef('http://schema.org/maxValue'),
    #             rdflib.term.URIRef('http://schema.org/minValue'),
    #             rdflib.term.URIRef('http://schema.org/name'),
    #             rdflib.term.URIRef('http://schema.org/valueReference'),
    #             rdflib.term.URIRef('http://www.w3.org/ns/ssn/isPropertyOf')
    #         ]
    #
    #         expected_multiple_predicates_for_current_subject = {
    #             rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
    #         }
    #
    #         (predicates_for_current_subject_list,
    #          multiple_predicates_for_current_subject) = rdf_to_dict.get_predicates_for_current_subject(current_subject,
    #                                                                                                    self.graph)
    #         self.assertEqual(expected_predicates_for_current_subject_list, predicates_for_current_subject_list)
    #         self.assertEqual(expected_multiple_predicates_for_current_subject, multiple_predicates_for_current_subject)
    #
    #     def test_02(self) -> None:
    #         current_subject = rdflib.term.URIRef(
    #             'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/SensorCapability')
    #
    #         expected_predicates_for_current_subject_list = [
    #             rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
    #             rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
    #             rdflib.term.URIRef('http://schema.org/name'),
    #             rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#comment'),
    #             rdflib.term.URIRef('http://www.w3.org/ns/ssn/hasProperty'),
    #             rdflib.term.URIRef('http://www.w3.org/ns/ssn/hasProperty'),
    #             rdflib.term.URIRef('http://www.w3.org/ns/ssn/hasProperty')
    #         ]
    #
    #         expected_multiple_predicates_for_current_subject = {
    #             rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
    #             rdflib.term.URIRef('http://www.w3.org/ns/ssn/hasProperty')
    #         }
    #
    #         (predicates_for_current_subject_list,
    #          multiple_predicates_for_current_subject) = rdf_to_dict.get_predicates_for_current_subject(current_subject,
    #                                                                                                    self.graph)
    #         self.assertEqual(expected_predicates_for_current_subject_list, predicates_for_current_subject_list)
    #         self.assertEqual(expected_multiple_predicates_for_current_subject, multiple_predicates_for_current_subject)

    # class Testget_subject_literal_list_dict(unittest.TestCase):
    #     # TODO: maybe check also the worked_triples
    #     graph, redirect_file_url_cleaned = utilities.load_git_rdf(persistent_id_url=persistent_id_url)
    #
    #     def test_00(self) -> None:
    #         current_subject = rdflib.term.URIRef('https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8')
    #
    #         (predicates_for_current_subject_list,
    #          multiple_predicates_for_current_subject) = rdf_to_dict.get_predicates_for_current_subject(current_subject,
    #                                                                                                    self.graph)
    #
    #         namespaces = set(self.graph.namespaces())
    #         worked_triples = set()
    #         sub_temp_dict, worked_triples = rdf_to_dict.get_subject_literal_list_dict(current_subject,
    #                                                                                   multiple_predicates_for_current_subject,
    #                                                                                   self.graph, namespaces,
    #                                                                                   worked_triples)
    #
    #         expected_sub_temp_dict = {'0184ebd9-988b-7bba-8203-06be5cf6bbb8': {'prefix': 'https://w3id.org/fst/resource/',
    #                                                                            'keywords': {
    #                                                                                'prefix': 'http://schema.org/',
    #                                                                                'literal': sorted(
    #                                                                                    ['Druck', 'Piezoresistiv',
    #                                                                                     'absolut']),
    #                                                                            },
    #                                                                            'identifier': {
    #                                                                                'prefix': 'http://purl.org/dc/terms/',
    #                                                                                'literal': sorted([
    #                                                                                    '0184ebd9-988b-7bba-8203-06be5cf6bbb8',
    #                                                                                    'fst-inv:D092']),
    #                                                                            },
    #                                                                            },
    #                                   }
    #
    #         self.assertEqual(expected_sub_temp_dict, sub_temp_dict)
    #
    #     def test_01(self) -> None:
    #         current_subject = rdflib.term.URIRef(
    #             'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/SensorCapability')
    #
    #         (predicates_for_current_subject_list,
    #          multiple_predicates_for_current_subject) = rdf_to_dict.get_predicates_for_current_subject(current_subject,
    #                                                                                                    self.graph)
    #
    #         namespaces = set(self.graph.namespaces())
    #         worked_triples = set()
    #         sub_temp_dict, worked_triples = rdf_to_dict.get_subject_literal_list_dict(current_subject,
    #                                                                                   multiple_predicates_for_current_subject,
    #                                                                                   self.graph, namespaces,
    #                                                                                   worked_triples)
    #
    #         expected_sub_temp_dict = {'SensorCapability': {
    #                                         'prefix': 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/',
    #                                     }
    #                                  }
    #
    #         self.assertEqual(expected_sub_temp_dict, sub_temp_dict)
    #
    #

# class Testget_temp_dict(unittest.TestCase):
#     # TODO: maybe check also the worked_triples
#     graph, redirect_file_url_cleaned = utilities.load_git_rdf(persistent_id_url=persistent_id_url)
#
#     def test_00(self) -> None:
#         current_subject = rdflib.term.URIRef(
#             'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/Sensitivity')
#         worked_triples = set(self.graph.triples((rdflib.term.URIRef('https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/SensorCapability'), None, None)))
#
#         temp_dict, worked_triples = rdf_to_dict.get_temp_dict(current_subject, self.graph, worked_triples)
#         parsed_temp_sub_dict = temp_dict['Sensitivity']
#
#         expected_temp_sub_dict = \
#             expected_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['hasSystemCapability']['SensorCapability'][
#                 'hasProperty']['Sensitivity']
#
#
#         # Check if the main element in the dict has the same keys
#         self.assertEqual(sorted(expected_temp_sub_dict.keys()), sorted(parsed_temp_sub_dict.keys()))
#
#         self.assertEqual(expected_temp_sub_dict, parsed_temp_sub_dict)
#
#     def test_04(self) -> None:
#         # Check if the main element in the dict has the same keys
#         current_subject = rdflib.term.URIRef(
#             'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/SensorCapability')
#         worked_triples = set()
#         # worked_triples = set(self.graph.triples((rdflib.term.URIRef(
#         #     'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8/SensorCapability'), None, None)))
#
#         temp_dict, worked_triples = rdf_to_dict.get_temp_dict(current_subject, self.graph, worked_triples)
#         parsed_temp_sub_dict = temp_dict['SensorCapability']
#
#         expected_temp_sub_dict = \
#             expected_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['hasSystemCapability']['SensorCapability']
#
#         # Check if the main element in the dict has the same keys
#         self.assertEqual(sorted(expected_temp_sub_dict.keys()), sorted(parsed_temp_sub_dict.keys()))
#
#         self.assertEqual(expected_temp_sub_dict, parsed_temp_sub_dict)
#
#     def test_01(self) -> None:
#         # Check if a small sub dict is equal
#         self.assertEqual(self.expected_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['type'],
#                          self.parsed_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['type'])
#
#     def test_02(self) -> None:
#         # Check if a small sub dict is equal
#         expected_dict = self.expected_dict
#         parsed_dict = self.parsed_dict
#
#         expected_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['identifier']['literal'] = (
#             sorted(expected_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['identifier']['literal']))
#         parsed_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['identifier']['literal'] = (
#             sorted(parsed_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['identifier']['literal']))
#
#         self.assertEqual(expected_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['identifier'],
#                          parsed_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['identifier'])
#
#     def test_03(self) -> None:
#         # Check if the main element in the dict has the same keys
#         self.assertEqual(
#             sorted(self.expected_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['hasSystemCapability'].keys()),
#             sorted(self.parsed_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['hasSystemCapability'].keys()))
#

#
#     # def test_05(self) -> None:
#     #     # Check if a small sub dict is equal
#     #     self.assertEqual(self.expected_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['type'],
#     #                      self.parsed_dict['0184ebd9-988b-7bba-8203-06be5cf6bbb8']['type'])
#