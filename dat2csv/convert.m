addpath(genpath('./Functions/'))

[File, Path] = uigetfile('*.dat','MultiSelect','on');

if isa(File, 'cell') % Multiple files selected
    for idx = 1:length(File)
        process_dat(File{idx}, Path)
    end
elseif File ~= 0 % One file selected
    process_dat(File, Path)
else
    error('No files are selected')
end
