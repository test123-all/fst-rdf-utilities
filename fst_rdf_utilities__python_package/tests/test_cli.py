import unittest
from pathlib import Path

from fst_rdf_utilities_py import utilities

from cli import parse_online_RDF_and_save_as_mat

# Setup environment
file_directory_path: Path = Path(__file__).resolve().parent
cached_data_sets_directory_path: Path = Path(file_directory_path / '_cached_data_sets')
try:
    cached_data_sets_directory_path.mkdir()
except FileExistsError:
    pass

class TestCLI(unittest.TestCase):
    # TODO: FIXME: Add a configuration file where the access token can be stored, that it wont be comitted to the
    #  repository
    # TODO: Add test with a access token.
    access_token = ''


    def test_00(self) -> None:
        pID_url = 'https://w3id.org/fst/resource/018bb4b1-db48-73b8-9d82-8a8ffb6ee225'
        parse_online_RDF_and_save_as_mat(persistent_ID_URL=pID_url,
                                         cached_data_sets_directory_path=cached_data_sets_directory_path)
                                         # access_token=self.access_token)

    def test_01(self) -> None:
        pID_url = 'https://w3id.org/fst/resource/018bb4b1-db4a-7bbd-a299-ee3b49b5d7f5'
        parse_online_RDF_and_save_as_mat(persistent_ID_URL=pID_url,
                                         cached_data_sets_directory_path=cached_data_sets_directory_path)
                                         # access_token=self.access_token)

    def test_02(self) -> None:
        url = 'https://git.rwth-aachen.de/fst-tuda/public/metadata/unit_under_test_rexer_public/-/raw/main/018bfcec-503e-7bcb-a136-7edf30722bf6/rdf.ttl'
        rdf_file_content, version_commit_id = utilities.get_GitLab_file_content_and_version_commit_id(url, self.access_token)
