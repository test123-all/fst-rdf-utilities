import unittest
from pathlib import Path
import rdflib


from rdf_test import rdf_git_repository


class TestRepo(unittest.TestCase):
    def test_script(self) -> None:
        path_to_repository = Path('/home/sebastian/Desktop/metadata_hub/')
        rdf_git_repository.load_rdf_data_repository(root_path=str(path_to_repository))