function p_ID_url_name = convertPIDURLToMatlabName(pID_url)
pID_url_cleaned = strrep(pID_url, '"', '');
% newStr = strrep(pID_url_cleaned, '/', '_');
% newStr = strrep(newStr, '.', '_');
% newStr = strrep(newStr, ':', '_');
pID_url_cleaned_splitted_array = split(pID_url_cleaned, '/');
newStr = pID_url_cleaned_splitted_array(end);
p_ID_url_name = ['pID_', char(strrep(newStr, '-', '_'))];

end