#!/bin/python3
import argparse
from pathlib import Path

from fst_rdf_utilities__python_package.fst_rdf_utilities_py import utilities
from fst_rdf_utilities__python_package.fst_rdf_utilities_py import rdf_to_dict


def set_up_CLI():
    parser = argparse.ArgumentParser()
    parser.add_argument("persistent_ID_URL")
    parser.add_argument('--access_token', dest='access_token',
                        required=False, default=None,
                        help=('The access token to your git instance '
                              'account (GitLab, Github, and so on) to be '
                              'able to load private RDF datasets.'))
    args = parser.parse_args()
    return args


def parse_online_RDF_and_save_as_mat(persistent_ID_URL: str,
                                     cached_data_sets_directory_path: (Path, str),
                                     access_token: str=None):
    # TODO check if the URL is a URL and a persistent one
    if access_token:
        online_rdf_dict, main_subject_uuid = rdf_to_dict.parse_online_RDF_to_dict(persistent_ID_URL,
                                                                                  access_token=access_token)
    else:
        online_rdf_dict, main_subject_uuid = rdf_to_dict.parse_online_RDF_to_dict(persistent_ID_URL)

    utilities.save_online_RDF_dict_as_mat_file(pID_url=persistent_ID_URL,
                                               online_rdf_dict=online_rdf_dict[main_subject_uuid],
                                               save_to_directory_path=cached_data_sets_directory_path)


def main():
    # Testable with command $ poetry run python cli.py "https://w3id.org/fst/resource/0184ebd9-988b-7bb9-bf0b-8ac992cecf10"
    args = set_up_CLI()

    # Set up the environment
    file_directory_path: Path = Path(__file__).resolve().parent
    cached_data_sets_directory_path: Path = Path(file_directory_path / '_cached_data_sets')
    try:
        cached_data_sets_directory_path.mkdir()
    except FileExistsError:
        pass

    # Run the function
    # Note: At this place there would be room to extend the CLI by different functions
    if args.access_token:
        parse_online_RDF_and_save_as_mat(persistent_ID_URL=args.persistent_ID_URL,
                                         cached_data_sets_directory_path=cached_data_sets_directory_path,
                                         access_token=args.access_token)
    else:
        parse_online_RDF_and_save_as_mat(persistent_ID_URL=args.persistent_ID_URL,
                                         cached_data_sets_directory_path=cached_data_sets_directory_path)


if __name__ == '__main__':
    main()
