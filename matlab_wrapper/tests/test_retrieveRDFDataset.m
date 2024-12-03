% Set up environment
file_dir_path = fileparts(mfilename('fullpath'));
path_to_the_config_file = [file_dir_path, '\..\..\EXAMPLE.config.json'];

% test 00 without acces key
test_pid_URL_00 = 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8';
[file_name_00, pID_sensor_00] = retrieveRDFDataset(test_pid_URL_00);

% test 01 with access key
test_pid_URL_01 = 'https://w3id.org/fst/resource/1ed6c2f8-282a-64b4-94d0-4ee51dfba10e';
[file_name_01, pID_sensor_01] = retrieveRDFDataset(test_pid_URL_01, 'config_json_file_path', path_to_the_config_file);

% test 02 with access key
test_pid_URL_02 = 'https://w3id.org/fst/resource/018bb4b1-db4a-7bbd-a299-ee3b49b5d7f5';
[file_name_02, pID_sensor_02] = retrieveRDFDataset(test_pid_URL_02, 'config_json_file_path', path_to_the_config_file);