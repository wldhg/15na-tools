addpath(genpath('./Functions/'));

[File, Path] = uigetfile('*.dat','MultiSelect','on');

if isa(File, 'cell') % Multiple files selected
    for idx = 1:length(File)
        fprintf('Processing ' + File{idx} + '.\n');
        process_dat(File{idx}, Path);
    end
elseif File ~= 0 % One file selected
    fprintf('Processing ' + File + '.\n');
    process_dat(File, Path);
else
    error('No file is selected');
end
