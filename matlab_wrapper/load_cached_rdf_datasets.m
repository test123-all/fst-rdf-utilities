function rdf_data_struct = load_cached_rdf_datasets()
full_filepath = mfilename('fullpath');
[dirpath,~,~] = fileparts(full_filepath);
cached_data_sets_dir_path = [dirpath, '\rdf_test\_cached_data_sets'];
file_list = dir(cached_data_sets_dir_path);

rdf_data_struct = struct();
for ii = 1:length(file_list)
    [~,~,ext] = fileparts(file_list(ii).name);
    if strcmp(ext, '.mat')
        temp_data = load([cached_data_sets_dir_path, '\', file_list(ii).name]);
        rdf_data_struct = combineStructs(rdf_data_struct, temp_data);
    end
end
