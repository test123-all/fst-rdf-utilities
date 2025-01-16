<!-- heading declaration and main RDFa data declaration in HTML-->
<div xmlns:schema="https://schema.org/" typeof="schema:SoftwareSourceCode" id="software-1">
    <h1 property="schema:name">FST RDF utilities</h1>
    <meta property="schema:codeRepository" content="https://github.com/test123-all/fst-rdf-utilities">
    <meta property="schema:codeSampleType" content="full solution">
    <meta property="schema:license" content="https://opensource.org/license/mit">
    <meta property="schema:programmingLanguage" content="Python, Matlab">
    <h2>Introduction:</h2>
    <p property="schema:description">
        This is the repository of the FST RDF utilities, a Python package/software with a wrapper for Mathworks Matlab
        that is able to load RDF graphs given by a main node into Python dictionaries and matlab structs to be able to
        load and use a subset of RDF data more easily and efficiently without the need to break long-established and
        intuitive data usage habits in Python and Mathworks Matlab. The program needs to start the mapping of the graph
        into a hierarchical data structure at one main node and will traverse and load all subnodes, their sub-nodes
        and so on, that are connected and directed away from them until there are no nodes left or got already used in
        the graph. <br>
        <br>
        For more information about how this software is used in an open source information infrastructure please refer
        to the following paper:
        <ol>
            <li>
                <div>
                    <strong>
                        <span property="schema:name">How to Make Bespoke Experiments FAIR: Modular Dynamic Semantic 
                        Digital Twin and Open Source Information Infrastructure</span>
                        <span>(</span>
                        <a property="schema:relatedLink" href="https://preprints.inggrid.org/repository/view/40/" typeof="schema:Article"> 
                            <span>https://preprints.inggrid.org/repository/view/40/</span>
                        </a>
                        <span>)</span>
                    </strong>
                    <span>(January 2025, currently only available as a preprint.)</span>
                </div>
          </li>
        </ol>
    </p>
</div>


<b>DISCLAIMER:</b> <br>
This software in its current version is in an early proof of concept phase and directly used, mentioned and explained in the 
https://preprints.inggrid.org/repository/view/40/ paper. This first raw work in progress version was used to achieve the
results mentioned in the paper.<br>
<br>
Since this software is in an early proof of concept phase it is not commented out comprehensively yet,
the functional segregation isn't good and in conclusion the function and variable names might be subject to 
significant change in the future. Therefore, the backwards compatibility of the API won't be granted for now. <br>
<br>
Please note that we are no longer able to provide an exact time span for the refactoring work at this time, as the 
German government has recently reduced funding for scientific purposes overall, leaving the future of all sciences 
somewhat uncertain. Thank you very much for your understanding.


## How to use this package?:
Before you start, please make sure that in your Python environment the 'fst_rdf_utilities_py' Python package is
installed and the dependencies mentioned in the 'Dependencies:' Section of this README.md file.

In Python:
```python
from pathlib import Path

from rdflib import URIRef
from fst_rdf_utilities_py import rdf_to_dict


# From a web source.
# Please NOTE: The access token is optional. And could be replaced by a acess_token file in the future,
#  that the users won't accidently commit their token openly into git projects.
persistent_id_url = 'https://w3id.org/fst/resource/064f05d1-5d2d-7a6f-8000-a3da10f5a1a3'
online_rdf_dict, main_subject_uuid = parse_online_RDF_to_dict(persistent_id_url=persistent_id_url, access_token=None)


# From a local file.
path_to_local_RDF_ttl_file = Path('./064f05d1-5d2d-7a6f-8000-a3da10f5a1a3_RDF_file.ttl')
main_subject = URIRef('https://w3id.org/fst/resource/064f05d1-5d2d-7a6f-8000-a3da10f5a1a3')
main_subject_prefix = 'https://w3id.org/fst/resource/'

rdf_dict_from_local_file = parse_RDF_file_to_dict(file_path=path_to_local_RDF_ttl_file, main_subject=main_subject, main_subject_prefix=main_subject_prefix)

```

Mathworks Matlab (please make sure to adjust the path seperators accordingly to your operating system standards):
```matlab
% Set up environment
path_to_the_config_file = '.\EXAMPLE.config.json';

% Without access token
p_ID_URL_00 = 'https://w3id.org/fst/resource/064f05d1-5d2d-7a6f-8000-a3da10f5a1a3';
[file_name_00, p_ID_sensor_00] = retrieveRDFDataset(p_ID_URL_00);

% With access token
p_ID_URL_00 = 'https://w3id.org/fst/resource/064f05d1-5d2d-7a6f-8000-a3da10f5a1a3'; % You should choose a resource that is only accessible through an access token
[file_name_01, p_ID_sensor_01] = retrieveRDFDataset(p_ID_URL_01, 'config_json_file_path', path_to_the_config_file);
```

## Possible Improvements:
The following list includes some possible improvements that have been identified up to this version, but it is non-exhaustive:
1. TODO: Search for additional possible use cases and functions followed by a reevaluation of the current software.
2. TODO: After this do a restructuring and extensive refactoring of the existing code (add docstrings to the
refactored functions, test case clean up and documentation).


## Dependencies:
The Python package uses the following third-party Python packages as dependencies:
- rdflib _ BSD License (BSD-3-Clause) (https://pypi.org/project/rdflib/ [Last Access at 16th January 2025])
- scipy _ BSD License (https://pypi.org/project/scipy/ [Last Access at 16th January 2025])
- beautifulsoup4 _ MIT License (https://pypi.org/project/beautifulsoup4/ [Last Access at 16th January 2025])
- requests _ Apache License, Version 2.0 (https://pypi.org/project/requests/ [Last Access at 16th January 2025])
- validators _ MIT License (https://pypi.org/project/validators/ [Last Access at 16th January 2025])
- arrow _ Apache License, Version 2.0 (https://pypi.org/project/arrow/ [Last Access at 16th January 2025])

The matlab wrapper around the Python package also uses:
- fst-matlab-struct-utilities _ MIT License (https://github.com/test123-all/fst-matlab-struct-utilities [Last Access at 16th January 2025])


<!-- maintainer- and creator- RDFa data declaration in HTML-->
<div xmlns:schema="https://schema.org/" about="#software-1">
    <h2>Current Maintainer[s]:</h2>
    <div typeof="schema:Person">
        <strong property="schema:givenName">Sebastian</strong>
        <strong property="schema:familyName">Neumeier</strong>
        <strong>(<a href="https://orcid.org/0000-0001-9533-9004" property="schema:identifier">https://orcid.org/0000-0001-9533-9004</a>)</strong>
        <span property="schema:email">sebastian.neumeieratstud.tu-darmstadt.de</span>
    </div>
    <h2>Authors:</h2>
    <p xmlns:dcterms="http://purl.org/dc/terms/">The first running version of this software was originally created in 
         <span property="dcterms:date" content="2023-04-01">February 2024</span>
         by:
    </p>
    <div typeof="schema:Person">
        <strong property="schema:givenName">Sebastian</strong>
        <strong property="schema:familyName">Neumeier</strong>
        <strong>(<a href="https://orcid.org/0000-0001-9533-9004" property="schema:identifier">https://orcid.org/0000-0001-9533-9004</a>)</strong>
        , <span property="schema:affiliation">
            Chair of Fluid Systems at Technical University of Darmstadt 
            (<a href="https://ror.org/05n911h24">https://ror.org/05n911h24</a>)
        </span>
        : <span property="schema:role">Conceptualization, Implementation, Documentation</span>.
    </div>
    <div typeof="schema:Person">
        <strong property="schema:givenName">Manuel</strong>
        <strong property="schema:familyName">Rexer</strong>
        <strong>(<a href="https://orcid.org/0000-0003-0559-1156" property="schema:identifier">https://orcid.org/0000-0003-0559-1156</a>)</strong>
        , <span property="schema:affiliation">
            Chair of Fluid Systems at Technical University of Darmstadt 
            (<a href="https://ror.org/05n911h24">https://ror.org/05n911h24</a>)
        </span>
        : <span property="schema:role">Project Manager, Provider of Use Cases and Requirements</span>.
    </div>
</div>


## Additional Ressources:
This software is somehow connected to the following paper[s] or contributed to the results of the following papers:
<ol>
   <li>
       <div>
           <strong>
               <span property="schema:name">How to Make Bespoke Experiments FAIR: Modular Dynamic Semantic Digital Twin and Open Source Information Infrastructure</span>
               <span>(</span>
               <a property="schema:relatedLink" href="https://preprints.inggrid.org/repository/view/40/" typeof="schema:Article"> 
                   <span>https://preprints.inggrid.org/repository/view/40/</span>
               </a>
               <span>)</span>
           </strong>
           <span>(January 2025, currently only available as a preprint.)</span>
       </div>
   </li>
</ol>
