addpath(genpath('./Functions/'));

fprintf('Select X (csv) file\n');
[CSVFile, CSVPath] = uigetfile('*.csv','MultiSelect','on');

fprintf('Select Raw Y (y) file\n');
[YFile, YPath] = uigetfile('*.y', 'MultiSelect', 'on');

if isa(CSVFile, 'cell') & isa(YFile, 'cell') % Multiple files selected
    if length(CSVFile) ~= length(YFile) % The number of CSV & Y files not matching
        error('Please select the same number of files for CSV & Y');
    else
        CSVFile = sortrows(CSVFile');
        YFile = sortrows(YFile');
        for idx = 1:length(CSVFile)
            fprintf("Processsing " + CSVFile{idx} + " & " + YFile{idx} + ".\n");
            datName = strrep(CSVFile{idx}, '.csv', '');
            datName = strrep(datName, 'csi_', '');
            yName = strrep(YFile{idx}, '.y', '');
            if (~strcmp(datName, yName)) % File name not matching
                error('Please name CSV files and Y files equally.');
            else
                process_y(CSVFile{idx}, CSVPath, YFile{idx}, YPath);
            end
        end
    end
elseif size(CSVFile) ~= 0 & size(YFile) ~= 0 % One file selected
    fprintf("Processing " + CSVFile + " & " + YFile + ".\n");
    process_y(CSVFile, CSVPath, YFile, YPath);
elseif size(YFile) ~= 0
    error('No CSV file (from .dat) is selected');
else
    error('No Y file is selected');
end
