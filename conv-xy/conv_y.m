addpath(genpath('./Functions/'));

fprintf('Select X (csv) file\n');
[CSVFile, CSVPath] = uigetfile('*.csv','MultiSelect','on');

fprintf('Select a Raw Y (y) file\n');
[YFile, YPath] = uigetfile('*.y', 'MultiSelect', 'off');

if isa(CSVFile, 'cell') % Multiple files selected\
    CSVFile = sortrows(CSVFile');
    for idx = 1:length(CSVFile)
        fprintf("Processsing " + CSVFile{idx} + " & " + YFile + "... ");
        process_y(CSVFile{idx}, CSVPath, YFile, YPath);
    end
elseif size(CSVFile) ~= 0 & size(YFile) ~= 0 % One file selected
    fprintf("Processing " + CSVFile + " & " + YFile + "... ");
    process_y(CSVFile, CSVPath, YFile, YPath);
elseif size(YFile) ~= 0
    error('No CSV file (from .dat) is selected');
else
    error('No Y file is selected');
end
