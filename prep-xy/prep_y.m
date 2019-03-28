addpath(genpath('./Functions/'));

fprintf('Select X (csv) file\n');
[CSVFile, CSVPath] = uigetfile('*.csv','MultiSelect','on');

fprintf('Select Raw Y (y) file\n');
[YFile, YPath] = uigetfile('*.y', 'MultiSelect', 'on');

if isa(CSVFile, 'cell') & size(YFile) ~= 0 % Multiple files selected
    for idx = 1:length(CSVFile)
        process_y(CSVFile{idx}, CSVPath{idx}, YFile, YPath);
    end
elseif size(CSVFile) ~= 0 & size(YFile) ~= 0 % One file selected
    process_y(CSVFile, CSVPath, YFile, YPath);
elseif size(YFile) ~= 0
    error('No CSV file(s) are selected');
else
    error('No Y file(s) are selected');
end
