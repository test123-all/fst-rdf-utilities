from copy import deepcopy
from pathlib import Path
import hashlib

import rdflib
import arrow

from .utilities import load_git_rdf
from .dict_utilities import combine_dicts_recursively, set_value_inside_nested_dict_with_path, get_value_inside_nested_dict_with_path


def _get_uuid_and_prefix(uriref: rdflib.term.URIRef, namespaces: set) -> (str, str):
    # TODO: FIXME: This function needs refactoring and a overhaul. There are codeblocks qhich are relly similar and
    #  could be refactored as function or at least in one if block
    # Get prefix + uuid
    # TODO: Check if the uriref is in the graph, it might be possible that it isn't in the graph but the prefix is used, which doesn't raise a error
    prefix = None
    uuid = None
    for item in namespaces:
        item_string = str(item[1])
        uriref_string = str(uriref)

        if item_string in uriref_string:
            prefix = item_string
            uuid = uriref_string.replace(item_string, '')
            break

    # There are possibilities where URIRefs get mentioned inside a file without declaring a prefix therefore prefix and uuid will be none
    if (prefix == None
            and uuid == None):
        uriref_string_splitted = str(uriref).split('/')
        prefix = '/'.join(uriref_string_splitted[:-1])
        uuid = uriref_string_splitted[-1]

    try:
        if '/' == uuid[0]:
            uuid = uuid[1:]

        if '/' == uuid[-1]:
            uuid = uuid[:-1]
    except TypeError:
        raise Exception('The given ')

    if '/' in uuid:
        uuid_splitted = uuid.split('/')
        uuid = uuid_splitted[-1]

        # Lösche alle / am Ende vom prefix
        while '/' == prefix[-1]:
            prefix = prefix[:-1]

        joined_together_uuid = "/".join(uuid_splitted[:-1])
        prefix = f'{prefix}/{joined_together_uuid}/'

    # Check if the uuid contains '.' if yes split it atgh the '.' symbol and use the last elemnt as uuid and append
    # the rest with the point to the prefix.
    if ('.' in uuid
            or len(uuid) > 32): # struct field names longer than 32 characters are forbidden in matlab
        # uuid_splitted = uuid.split('.')
        # prefix = f'{prefix}/{".".join(uuid_splitted[:-1])}.'
        # uuid = uuid_splitted[-1]
        prefix = f'{prefix}/{uuid}'  # combine the back together

        # Calculate the blake2s hash
        uuid_hex_hash = hashlib.blake2s(uuid.encode(encoding="UTF-8"), digest_size=32).hexdigest()
        uuid = f'FORBID_{uuid_hex_hash[:23]}' #
        
    return prefix, uuid
# Schritt 1 ist erstmal zu bekommen was der hauptnod ein der Datei ist
# Schritt 1.5 Erstelle eine iterated_tuples liste, die alle bereits iterierten tuple enthält
#### Iteration 1
# Schritt 2 alle tuple bekommen, die den hauptnode (current node) als subject haben
# Schritt 3 die tuple in das dict format parsen und (merken, dass ich sie benutzt habe (der iterated_tuples liste hinzufügen))
# Schritt 4 mir die Objekte in einer Liste merken
#### Iteration 2
# Schritt 5 Die Objekte als neue Subjekte (current nodes) verwenden und darüber iterieren


# Probleme:
# 1. was ist das Abbruchkriterium der Iteration? Wenn ich während einer Iteration alle Subjekte durchiteriert habe und die schon in der verwendet Liste sind -> finished flag
#   wenn nur ein übrig bleibt bekomme ich auch nur da neue objekte, die de rListe hinzugefügt werden.
# 2. Wie bzw. woher wieß ich wo ich die Elemente dann im dict einfügen muss?
# 3. wie funktioniert das parsen genau? Für ein triple https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8 .. Es muss unterschieden werden zwischen drei Fällen s,p,o(normal), s,p,o(als Literal), s,p,o,(als Literal Liste)


def _parse_subgraph_to_dict(subgraph: rdflib.Graph, subject: rdflib.term.URIRef):
    #distinct_predicates_set = _get_distinct_predicates_for_current_subject(subject, subgraph)
    distinct_predicates_set = set(subgraph.predicates(subject=subject))

    sub_dict = {}
    namespaces = set(subgraph.namespaces())

    # Parse to prefix and uuid.
    [current_subject_prefix, current_subject_uuid] = _get_uuid_and_prefix(subject, namespaces)

    # Create the first structure for the subject.
    if current_subject_uuid not in sub_dict.keys():
        sub_dict[current_subject_uuid] = {}
        sub_dict[current_subject_uuid]['prefix'] = current_subject_prefix
    else:
        print('shit1')

    for distinct_predicate in sorted(distinct_predicates_set):
        # Get all triples for the distinct subject and predicate and parse it in another graph to be able to easier work with
        [current_distinct_predicate_prefix, current_distinct_predicate_uuid] = _get_uuid_and_prefix(rdflib.URIRef(str(distinct_predicate)), namespaces)
        sub_dict[current_subject_uuid][current_distinct_predicate_uuid] = {}
        sub_dict[current_subject_uuid][current_distinct_predicate_uuid]['prefix'] = current_distinct_predicate_prefix

        #### Check if there are more than one triples if yes they all need to be URIRef or Literals
        sorted_triple_list = sorted(list(subgraph.triples((subject, distinct_predicate, None))))

        # Are all objects of them of type URIRef?
        URIRef_flag = True
        for triple in sorted_triple_list:
            if not isinstance(triple[2], rdflib.URIRef):
                URIRef_flag = False
                break

        # Are all objects of them of type Literal?
        Literal_flag = True
        for triple in sorted_triple_list:
            if not isinstance(triple[2], rdflib.Literal):
                Literal_flag = False
                break

        # Welche fälle können nicht auftreten? Beide True (enthält von beide etwas) oder beide False(enthält von beiden nichts, sollteenicht auftreten)
        # TODO: Make a second exception for the second case.
        if (URIRef_flag == True and Literal_flag == True
            or URIRef_flag == False and Literal_flag == False):
            raise Exception('There is a subject connected with a predicate to at least one URIRef and at least one Literal. This unambigous and forbidden!')
        ######

        # Es ist möglich, dass eins,p mehrere uriefs als objekte hat, wenn es ein literal ist
        # Es muss unterschieden werden zwischen drei Fällen s,p,o(normal), s,p,o(als Literal), s,p,o,(als Literal Liste)
        # CASE 1 s,p,o(normal)
        if URIRef_flag:
            for triple in sorted_triple_list:
                [current_object_prefix, current_object_uuid] = _get_uuid_and_prefix(rdflib.URIRef(str(triple[2])), namespaces)
                sub_dict[current_subject_uuid][current_distinct_predicate_uuid][current_object_uuid] = {}
                sub_dict[current_subject_uuid][current_distinct_predicate_uuid][current_object_uuid]['prefix'] = current_object_prefix
        # CASE 2 s,p,o(als Literal)
        # TODO: check wether all of them are literals
        elif Literal_flag:
            if len(sorted_triple_list) == 1:
                sub_dict[current_subject_uuid][current_distinct_predicate_uuid]['literal'] = sorted_triple_list[0][2].toPython()
                try:
                    sub_dict[current_subject_uuid][current_distinct_predicate_uuid]['datatype'] = sorted_triple_list[0][2].datatype.toPython()
                except AttributeError:
                    sub_dict[current_subject_uuid][current_distinct_predicate_uuid]['datatype'] = 'http://www.w3.org/2001/XMLSchema#string'

            # CASE 3 s,p,o,(als Literal Liste)
            # Check if for the current subject they are predicates that occur multiple times and all point to literals
            # and collect them in a list.
            elif len(sorted_triple_list) > 1:
                # Collect the literals in a list
                literal_list = []
                for literal_triple in sorted_triple_list:
                    literal_list.append(literal_triple[2].toPython())

                # Check the datatype of the list, they need to be equal
                try:
                    temp_datatype = literal_list[0].datatype
                except AttributeError:
                    temp_datatype = 'http://www.w3.org/2001/XMLSchema#string'

                for literal in literal_list:
                    try:
                        literal_datatype = literal.datatype
                    except AttributeError:
                        literal_datatype = 'http://www.w3.org/2001/XMLSchema#string'

                    if literal_datatype != temp_datatype:
                        raise Exception

                sub_dict[current_subject_uuid][current_distinct_predicate_uuid]['literal'] = sorted(literal_list)
                sub_dict[current_subject_uuid][current_distinct_predicate_uuid]['datatype'] = temp_datatype

    return sub_dict

def _parse_RDF_graph_to_dict(graph: rdflib.Graph, main_subject: rdflib.URIRef):
    # Schritt 1 ist erstmal zu bekommen was der hauptnod ein der Datei ist
    # -> main subject
    rdf_dict = {}

    # Schritt 1.5 Erstelle eine iterated_triple liste, die dann alle bereits iterierten tuple enthält
    subjects_list = []
    subject_dict = {'target': main_subject,
                    'path_to_target': '',
                   }
    subjects_list.append(subject_dict)

    while len(subjects_list) > 0:
        objects_list = []
        for subject in subjects_list:
            #### Iteration 1
            # Schritt 2 alle triple bekommen, die den hauptnode (current node) als subject haben und in sub graphen parsen
            triples = list(graph.triples((subject['target'], None, None)))
            temp_graph = rdflib.Graph(namespace_manager=graph.namespace_manager)

            namespaces = set(graph.namespaces())
            [_, current_subject_uuid] = _get_uuid_and_prefix(subject['target'], namespaces)
            # Add the triples to the temp graph to be able to parse them and remove them in the main graph
            for triple in triples:
                temp_graph.add(triple)
                graph.remove(triple)

                # Schritt 3 mir die URIRefObjekte und die Pfade dort hin in einer Liste merken
                objects_dict = {}
                if isinstance(triple[2], rdflib.URIRef):
                    objects_dict['target'] = triple[2]
                else:
                    continue

                [_, current_predicate_uuid] = _get_uuid_and_prefix(rdflib.URIRef(str(triple[1])), namespaces)
                [_, current_object_uuid] = _get_uuid_and_prefix(rdflib.URIRef(str(triple[2])), namespaces)

                objects_dict['path_to_target'] = f'{current_subject_uuid}.{current_predicate_uuid}' # .{current_object_uuid}

                if subject["path_to_target"] != '':
                    objects_dict['path_to_target'] = f'{subject["path_to_target"]}.{objects_dict["path_to_target"]}'

                objects_list.append(objects_dict)

            # Schritt 4 die tuple in das dict format parsen und (merken, dass ich sie benutzt habe (der iterated_tuples liste hinzufügen))
            sub_dict = _parse_subgraph_to_dict(subgraph=temp_graph, subject=subject['target'])

            # TODO: FIXME: es fehlt noch, dass ich weiß wo ich den subgraphen im main dict hinzufügen muss
            # Schritt 5 die sub_dict dem haupt dict hinzufügen
            # Woher weiß ich wo ich das hinzufügen muss? Ich kann mir den Weg zu dem object merken und in einem dict mit ablegen und das dann zum parsen nutzen
            # WARNING: FIXME: DIRTY WORKAROUND!
            if subject['path_to_target'] != '':
                # Jedesmal wenn der Pfad ungleich '' ist wird irgendwie etwas überschrieben
                value = get_value_inside_nested_dict_with_path(rdf_dict, subject['path_to_target'])
                if value is not None:
                    rdf_dict = set_value_inside_nested_dict_with_path(deepcopy(rdf_dict), subject['path_to_target'], combine_dicts_recursively(value, deepcopy(sub_dict)))

            else:
                rdf_dict = set_value_inside_nested_dict_with_path(deepcopy(rdf_dict), subject['path_to_target'], deepcopy(sub_dict))
            # In der ersten iteration ist es einfach nur '0184ebd9-988b-7bba-8203-06be5cf6bbb8' und dann kette ich prädikat uuid und objekt uuid aneinander.
            # und das muss ich mir dann auch in der objekt list mit weg speichern
        subjects_list = objects_list

    return rdf_dict

    #### Iteration 2
    # Schritt 5 Die Objekte als neue Subjekte (current nodes) verwenden und darüber iterieren


def parse_RDF_file_to_dict(file_path: [str, Path], main_subject: rdflib.URIRef, main_subject_prefix: str) -> dict:

    graph = rdflib.Graph(base=rdflib.URIRef(main_subject_prefix))
    # TODO: Check if file exists
    # TODO: Check if the main subject with the url exists in the file.
    # TODO: Check if the file is a .ttl file, that gets only supported for now

    with Path(file_path).open('r') as f:
        graph.parse(data=f.read(), format="turtle")

    rdf_dict = rdf_to_dict.parse_RDF_to_dict(graph=graph, main_subject=rdflib.URIRef(main_subject))  # 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8'

    return rdf_dict

def parse_online_RDF_to_dict(persistent_id_url: str, access_token: str =None) -> (dict, str):
    # TODO: That only works for normal requests that aren't to private files. For private files the API of gitlab needs to be used. This apis probably differ between all big git instances like GitLab, GitHub, Gitea, GitBucket, SourceForge, Gogs and so on
    # Wenn kein Token gegeben ist  kann ein normaler request benutzt werden, der für alle plattformen funktionieren sollte
    if not access_token:
        graph, version_commit_id = load_git_rdf(persistent_id_url)
    else:
        # Alternativ muss ein request über die API geschehen, die sich bei allen Plattformen wahrscheinlich unterscheided. D.h. es muss erstmal bestimmt werdne wlevhe platform es ist
        graph, version_commit_id = load_git_rdf(persistent_id_url, access_token=access_token)

    # Check if the main_subject exists as a subject in the graph
    main_subject = rdflib.URIRef('')
    for item in set(graph.subjects()):
        if str(item) == persistent_id_url:
            # Found the main subject
            main_subject: rdflib.URIRef = item
            break

    if str(main_subject) == '':
        raise Exception(
            "No main_subject was found, the rdf file you are trying to load doesn't seem to comply to the standards!")

    namespaces = graph.namespaces()
    [_, main_subject_uuid] = _get_uuid_and_prefix(main_subject, namespaces)

    online_rdf_dict = _parse_RDF_graph_to_dict(graph=graph, main_subject=rdflib.URIRef(main_subject))  # 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8'

    # Add the time to live metadata to the rdf_dict
    TTL = 1800  # seconds standard time dns cache time
    online_rdf_dict[main_subject_uuid]['dataset_METADATA'] = {
        'URI': persistent_id_url,
        'version_commit_hash': version_commit_id,
        'dataset_record_metadata': {
            'data_cached_at_timestamp': str(arrow.utcnow()),
            'TTL': {
                'name': 'time to life',
                'value': TTL,
                'unit': 's'
            }
        }
    }

    return online_rdf_dict, main_subject_uuid

