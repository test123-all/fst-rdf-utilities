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


# TODO check if the rdflib sparql result generator is convertable to a list,
# TODO: if yes check if there is always exactly one entity of something

def load_git_rdf(persistent_id_url: str) -> (rdflib.Graph, str):
    # TODO: check if the url alredy contains the .ttl or a similar ending
    # Get rdf data from the persistent_id_URI
    with requests.Session() as s:
        # 'https://w3id.org/fst/resource/0184ebd9-988b-7bb9-ae4b-17bd29feb36c'
        response = s.get(f'{persistent_id_url}.ttl')

    if response.headers['Content-Type'] == 'text/html; charset=utf-8':
        # Redirect through old html redirect
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tags = soup.find_all('meta')

        compiled_regex = re.compile('url=.* ')
        regex_output = compiled_regex.findall(str(meta_tags))
        redirect_url = regex_output[0].split('url=')
        redirect_file_url_cleaned = redirect_url[1].replace(' ', '').replace('"', '')

        with requests.Session() as s:
            response = s.get(redirect_file_url_cleaned)
            # TODO: The response is 'text/plain; charset=utf-8' and should be something like 'text/turtle; charset=utf-8'
            #  -> proposal for the new .html version

    # TODO: Add content negotiation
    g = rdflib.Graph()
    g.parse(redirect_file_url_cleaned, format="turtle", publicID=persistent_id_url)
    # g.parse(data=response.text, format="turtle", publicID=persistent_id_url)
    if redirect_file_url_cleaned:
        return [g, redirect_file_url_cleaned]
    else:
        return [g, response.request.url]


def load_sensor_rdf_and_parse_to_dict(persistent_id_url: str) -> [dict, str]:
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


def parse_url_into_parts(url) -> dict:
    # Split the URL in its parts
    # TODO: maybe replace https or
    parted_url = url.split('//')
    splitted_repository_url_list = parted_url[1].split('/-/')
    splitted_url = splitted_repository_url_list[0].split('/')
    splitted_file_path_url = splitted_repository_url_list[1].split('/')

    domain_address = splitted_url[0]
    base_url = f'https://{domain_address}'

    project_path_list = splitted_url[1:]
    project_path_url = ''
    for item in project_path_list:
        if project_path_url == '':
            project_path_url = f'{item}'
        else:
            project_path_url = f'{project_path_url}/{item}'

    file_path = ''
    for item in splitted_file_path_url[2:]:
        if file_path == '':
            file_path = f'{item}'
        else:
            file_path = f'{file_path}/{item}'

    return_variables_dict = {
        'base_url': base_url,
        'project_path_url': project_path_url,
        'repository_file_path': file_path
    }

    return return_variables_dict


def get_version_commit_hash(url):
    return_variables_dict = parse_url_into_parts(url)

    # Get wether the service lives on GitLab or something else
    # TODO: github gitea
    with requests.Session() as s:
        r = s.get(return_variables_dict['base_url'])
    soup = BeautifulSoup(r.text, 'html.parser')

    # ich möchte alle meta tags finden, die das property attribute haben
    def is_meta_tag_with_property_attribute(tag):
        # Filter funktion return true or false
        return tag.name == 'meta' and tag.has_attr('property') and tag['property'] == 'og:site_name'

    meta_site_name_soup = soup.find_all(is_meta_tag_with_property_attribute)
    if not meta_site_name_soup[0]['content'] == 'GitLab':
        raise Exception(f"{meta_site_name_soup[0]['content']} is currently not supported!")

    api_base_url = f"{return_variables_dict['base_url']}/api/v4/"

    #### Ab hier nur für GitLab
    # Get project id
    with requests.Session() as s:
        project_path_url_encoded = requests.utils.quote(return_variables_dict['project_path_url'], safe='')
        r = s.get(f"{api_base_url}/projects/{project_path_url_encoded}")

    projectid = r.json()['id']  # '84807'

    with requests.Session() as s:
        # /projects/:id/repository/files/:file_path
        URLencodedfilepath = requests.utils.quote(return_variables_dict['repository_file_path'], safe='')
        # TODO: FIXME: tokens from a token vault need to be used here
        # TODO: main branch is sleected, might be a problem in the future if useres aren't consistent with their branches
        # headers = {'PRIVATE-TOKEN': 'glpat-rFxz7TPcPugTsPSneuLk'}
        response = s.get(
            f'{api_base_url}/projects/{projectid}/repository/files/{URLencodedfilepath}?ref=main')  # , headers=headers)

        return response.json()['commit_id']


# def save_sensor_rdf_as_mat_file(pID_url: str, save_to_directory_path: [Path, str]) -> None:
#     [sensor_dict, redirect_file_url_cleaned] = load_sensor_rdf_and_parse_to_dict(pID_url)
#
#     TTL = 1800  # seconds standard time dns cache time
#     sensor_dict['UUID'] = {
#         'URI': sensor_dict['UUID'],
#         'version_commit_hash': get_version_commit_hash(redirect_file_url_cleaned),
#         'dataset_record_metadata': {
#             'data_cached_at_timestamp': str(arrow.utcnow()),
#             'TTL': {
#                 'name': 'time to life',
#                 'value': TTL,
#                 'unit': 's'
#             }
#         }
#     }
#
#     # Turn pid into name
#     # file_name = pID_url.replace('/', '_').replace('.', '_').replace(':', '_').replace('-', '_')
#     UUID = pID_url.split("/")[-1]
#     file_name = f'pID_{UUID.replace("-", "_")}'
#
#     test_dict = {f'{file_name}': sensor_dict}
#     # self.assertEqual(mat_struct['example_mat_struct'], x)
#     sio.savemat(f'{save_to_directory_path}/{file_name}.mat', test_dict)


def save_online_RDF_dict_as_mat_file(pID_url: str, online_rdf_dict: dict, save_to_directory_path: [Path, str]) -> None:
    # TODO: check wether the URL varaible is a url and a persistent one
    UUID = pID_url.split("/")[-1]
    file_name = f'pID_{UUID.replace("-", "_")}'

    save_dict = {f'{file_name}': online_rdf_dict}
    # self.assertEqual(mat_struct['example_mat_struct'], x)
    sio.savemat(f'{save_to_directory_path}/{file_name}.mat', save_dict)