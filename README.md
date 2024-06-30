# FST RDF utilities

## Introduction:
This is the repository of the FST RDF utilities, a python package/software with a wrapper for matlab that is able to load graphs given by a main node into python dictionaries and matlab structs to be able to load and use a subset of RDF data more easily and efficiently without the need to break long established and intuitive data usage habits in Python and Matlab. The program needs to start the mapping of the graph into a hierarchical data structure at one main node and will traverse and load all subnodes, their sub-nodes and so on, that are connected and directed away from them until there are no nodes left or got already used in the graph. <br>
<br>
<br>
<b>DISCLAIMER</b>:<br>
This software is in a early proof of concept phase and mentioned in the https://preprints.inggrid.org/repository/view/40/ paper. If you want to pay credit to this software in its current raw proof of concept state please cite the paper.<br>
<br>
Since this software is in a early proof of concept phase it is not commented out sufficiently yet, the functional segregation isn't good and in conclusion the function and variable names might be subject to siginificant change in the future. Therefore the backwards compatbility of the API won't be granted for now. <br>
<br>
As of the current plans the refactoring work will be done somewhere between the beginning of september 2024 and the end of december 2024 since the responsible person is a research aide and currently in exam phase. Thank you very much in advance for your understanding. <br>

## Current Maintainers:
sebastian.neumeieratstud.tu-darmstadt.de

## Creators:
This software was originally created by: <br>
**Sebastian Neumeier (https://orcid.org/0000-0001-9533-9004)**:  Conceptualization, Implementation, Documentation <br>
**Manuel Rexer (https://orcid.org/0000-0003-0559-1156)**: Project Manager, Provider of Use Cases and Requirements <br>
