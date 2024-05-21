%test_pid_URL = 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8';

function [file_name, pID_sensor] = retrieveRDFDataset(pID_url, varargin)

p = inputParser;
% TODO: Add a function validator that checks if the input is a char
addParameter(p, "config_json_file_path", "") % @(x)isChar);
parse(p, varargin{:});

access_token = '';
if ~strcmp(p.Results.config_json_file_path, "")
    fileID = fopen(p.Results.config_json_file_path, 'r');
    [A,~] = fscanf(fileID, '%s');

    json_value_struct = jsondecode(A);
    access_token = json_value_struct.access_token;
    fclose(fileID);
end

currentFileFullPath = mfilename('fullpath');
[dirpath,~,~] = fileparts(currentFileFullPath);
% Path to the testing environment
fst_rdf_utilities__python_package_path = [dirpath, '\..\fst_rdf_utilities__python_package'];

file_name = convertPIDURLToMatlabName(pID_url);

% TODO: make sure, that the cached data set gets ignored in the repository
mat_file_path =  [fst_rdf_utilities__python_package_path, '\_cached_data_sets\', file_name, '.mat'];
% Search for the .mat 
exists_returncode = exist(mat_file_path, 'file');

% Returns 0 if it doesn't exists
if exists_returncode ~= 0
    % ---- Evalin is really bad NOTE possible attack vector for a code ingestion attack! --------
    pID_sensor = load(mat_file_path);
    
    % If its already there check the timestamp and ttl and decide wether to reget the data
    timestamp_now = datetime('now', 'TimeZone', 'utc', 'Format', 'yyyy-MM-dd''T''HH:mm:ss:SSSSSSXXX');
    cached_dataset_timestamp = datetime(pID_sensor.(file_name).dataset_METADATA.dataset_record_metadata.data_cached_at_timestamp, 'InputFormat', 'yyyy-MM-dd''T''HH:mm:ss.SSSSSSXXX', 'TimeZone', 'utc', 'Format', 'yyyy-MM-dd''T''HH:mm:ss.SSSSSSXXX');
    cached_dataset_ttl_value = pID_sensor.(file_name).dataset_METADATA.dataset_record_metadata.TTL.value;
    
    calculated_difference = convertTo(timestamp_now, 'posixtime')  -  convertTo(cached_dataset_timestamp,'posixtime');
end

if exists_returncode == 0 || calculated_difference >= cached_dataset_ttl_value
    % ----- NOTE possible attack vector for a code ingestion attack! --------
    if ~strcmp(access_token, '')
        command = ['python ', fst_rdf_utilities__python_package_path, '\cli.py ', '--access_token "', char(access_token), '" "', char(pID_url), '"'];
        disp(command)
    else
        command = ['python ', fst_rdf_utilities__python_package_path, '\cli.py "', char(pID_url), '"'];
        disp(command)
    end
    
    [status,cmdout] = system(command);
    if status ~= 0
        error(['FST_ASAM_XIL_API ERROR: ', cmdout])
    end
    
    pID_sensor = load(mat_file_path);
end

% ----- NOTE possible attack vector for a code ingestion attack! --------
% geht scheinbar nicht einfach anders ohne die variable komplett global zu machen. Matlab ist absoluter drecks scheiß!
% command = ['if exist("pID_sensors") == 0;', ...
%             'pID_sensors = load("', mat_file_path, '");', ...
%            'else;', ...
%             'var = load("', mat_file_path, '");', ...
%             'pID_sensors.', file_name, '= var.', file_name, ';', ...
%            'end'];
% evalin('base', command);

end

% TODO: Es fehlt eien funktion mit der überprüft werden kann ob die python
% packages ordentlich installiert sind.
% TODO: es gibt noch probleme mit den Pfaden
% TODO: das laden dauert sehr lange pro Datei, evtl. darüber nachdenken
% die Zeit de rAbfrage in python mit aufzunehmen und eine standart
% intervall wie lange der wert gecached werden soll
