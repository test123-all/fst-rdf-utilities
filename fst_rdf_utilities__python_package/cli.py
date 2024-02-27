#!/bin/python3
import argparse
from pathlib import Path

from fst_rdf_utilities_py import utilities
from fst_rdf_utilities_py import rdf_to_dict


def main():
    # Testable with command $ poetry run python cli.py "https://w3id.org/fst/resource/0184ebd9-988b-7bb9-bf0b-8ac992cecf10"
    file_directory_path: Path = Path(__file__).resolve().parent
    cached_data_sets_directory_path: Path = Path(file_directory_path / '_cached_data_sets')
    try:
        cached_data_sets_directory_path.mkdir()
    except FileExistsError:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("persistent_ID_URL")
    args = parser.parse_args()

    # TODO check if the URL is a URL and a persistent one
    online_rdf_dict, main_subject_uuid = rdf_to_dict.parse_online_RDF_to_dict(args.persistent_ID_URL)

    utilities.save_online_RDF_dict_as_mat_file(pID_url=args.persistent_ID_URL,
                                               online_rdf_dict=online_rdf_dict[main_subject_uuid],
                                               save_to_directory_path=cached_data_sets_directory_path)


if __name__ == '__main__':
    main()
