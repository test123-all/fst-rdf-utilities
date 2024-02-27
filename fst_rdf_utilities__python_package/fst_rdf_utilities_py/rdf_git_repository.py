import os
from pathlib import Path
import rdflib
from os import walk
# Get all
# TODO: #########################################################################################
# TODO: Eigentlich müsste das eine Graph Klasse sein, die die zusätzlichen Funktionen unterstützt
# TODO: #########################################################################################

def load_rdf_data_repository(root_path: [str, Path]) -> [rdflib.ConjunctiveGraph, dict]:
    # FIXME: TODO: Get the base correctly
    conjunctive_context_graph = rdflib.ConjunctiveGraph(default_graph_base='https://w3id.org/fst/resource/')

    # FIXME: TODO: Such dir zwei Beispieldateien und schreibe Tests für diese Dateien!


    # TODO: Wie find eich en base pfad von einer Datei herraus?
    # TODO: Kann ich die namespace prefixes irgendwie mit laden?
    # TODO: was passiert bei überschneidungen wenn der prefix öfter verwendet wird -> bind befehl ankucken. Evtl. wird eine 1 angehängt
    # TODO: Warum sind die Namespaces so durcheinander?? Manchmal wird eine 1 angehängt. Warum?
    # conjunctive_context_graph.bind('dbo', rdflib.Namespace('http://dbpedia.org/ontology/'), override=True, replace=False)
    # conjunctive_context_graph.bind('qudt', rdflib.Namespace('http://qudt.org/schema/qudt/'), override=True, replace=False)
    # conjunctive_context_graph.bind('quantitykind', rdflib.Namespace('http://qudt.org/vocab/quantitykind/'), override=True,
    #                         replace=False)
    # conjunctive_context_graph.bind('schema', rdflib.Namespace('http://schema.org/'), override=True, replace=True)

    context_uri_namespace_dict: dict = dict()

    #pattern = re.compile(r'.*\.rdf$')
    for (dirpath, dirnames, filenames) in walk(str(root_path), topdown=True):
        # TODO: Test if there are multiple .rdf files and print a warning
        found_rdf_filenames = []
        for filename in filenames:
            if '.ttl' in filename:
                found_rdf_filenames.append(filename)

        if len(found_rdf_filenames) == 0:
            continue

        # Not 0 and not 1
        if len(found_rdf_filenames) != 1:
            # TODO: find a more suitable exception name
            raise Exception


        # Load .rdf file in a graph
        filepath = Path(f'{dirpath}/{found_rdf_filenames[0]}')
        context_uri_string :str = str(filepath)
        context_uri = rdflib.URIRef(context_uri_string)
        temp_g = rdflib.Graph(bind_namespaces='none', base='https://w3id.org/fst/resource/') #
        temp_g.parse(filepath.resolve(), format='ttl')

        contexted_subgraph = conjunctive_context_graph.get_context(identifier=context_uri, base=temp_g.base)

        # Speichere alle namespaces in einem dictionary
        context_uri_namespace_dict[context_uri_string]: dict = dict()
        for prefix, namespace in temp_g.namespaces():
            context_uri_namespace_dict[context_uri_string][prefix] = namespace
            # contexted_subgraph.bind(prefix, namespace, override=True, replace=True)
            print(prefix, namespace)
        #
        # contexted_subgraph.bind('dbo', rdflib.Namespace('http://dbpedia.org/ontology/'), override=True, replace=False)
        # contexted_subgraph.bind('qudt', rdflib.Namespace('http://qudt.org/schema/qudt/'), override=True, replace=False)
        # contexted_subgraph.bind('quantitykind', rdflib.Namespace('http://qudt.org/vocab/quantitykind/'), override=True, replace=False)
        # contexted_subgraph.bind('schema', rdflib.Namespace('http://schema.org/'), override=True, replace=True)

        for triple in temp_g:
            contexted_subgraph.add((triple[0], triple[1], triple[2]))

    return conjunctive_context_graph, context_uri_namespace_dict

def save_rdf_data_repository(conjunctive_context_graph: rdflib.ConjunctiveGraph, context_uri_namespace_dict: dict):
    ################################### Check if the triples stayed in the context, if yes thats great and a parsing to file function is possible
    # TODO: why it wouldn't be possible if they have changed?
    for quad in cg.quads():
        if (isinstance(quad[2], rdflib.Literal)
                and str(quad[2]) == 'Manuel'):
            print(f'{quad[2]}, {quad[3]}\n')

    # Für jeden Context den Graph bekommen und den Graph serialisieren.
    for subgraph in conjunctive_context_graph.contexts():
        filepath = str(subgraph.identifier)

        print(list(subgraph.namespaces()))
        # TODO: assign the namespaces from the context_uri_namespace_dict to match them what was got read out of the file
        # TODO: get the context uri string
        # TODO: The base URL somehow needs to be get too
        # context_uri_namespace_dict[context_uri_string][prefix]
        # for prefix in context_uri_namespace_dict[context_uri_string].keys():




        subgraph.serialize(destination=filepath, base=rdflib.URIRef('https://w3id.org/fst/resource/'),
                           format="longturtle")


    # FIXME: TODO: Test hinzufügen, das eine File auf Änderungen test und nur die Änderung und alles andere gleich bleibt, die namespaces z.B.
    # TODO: Der Test könnte z.B. so aussehen:
    list(cg.contexts())
    len(list(cg.contexts()))


    sparql_query = """
    PREFIX dbo: <http://dbpedia.org/ontology/>

    SELECT ?wimi
    WHERE {
    ?id dbo:maintainedBy ?wimi .

    }
    """
    qres = cg.query(sparql_query)
    list(qres)


    sparql_query = """
    DELETE {
        GRAPH ?g {?s ?p ?o } .
    }
    INSERT {
        GRAPH ?g {?s ?p "M. Rexer"} .
    }
    WHERE {
        GRAPH ?g {?s ?p ?o } .
        FILTER (isLiteral(?o) && STR(?o) = "Rexer")
    }
    """
    qres = cg.update(sparql_query)


    sparql_query = """
    PREFIX dbo: <http://dbpedia.org/ontology/>

    SELECT ?wimi
    WHERE {
    ?id dbo:maintainedBy ?wimi .

    }
    """
    qres = cg.query(sparql_query)
    list(qres)
