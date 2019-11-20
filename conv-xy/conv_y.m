addpath(genpath('./functions/'));

fprintf('Select converted CSI file(s) (.csv)\n');
[CSIFile, CSIPath] = uigetfile('*.csv','MultiSelect','on');

fprintf('Select labeling file(s) (.y)\n');
[LabelFile, LabelPath] = uigetfile('*.y', 'MultiSelect', 'on');

if isa(CSIFile, 'cell') % Multiple files selected
  CSIFile = sortrows(CSIFile');
  LabelFile = sortrows(LabelFile');
  if (length(CSIFile) == length(LabelFile))
    for idx = 1:length(CSIFile)
      fprintf("[Match] %s - %s\n", CSIFile{idx}, LabelFile{idx});
    end
    answ = questdlg('Check the stdout. Is the matching correct?', ...
      'Confirm', 'No', 'Yes', 'Yes');
    if strcmp(answ, 'No') == 1
      error('Select again with file name order matching!');
    else
      for idx = 1:length(CSIFile)
        process_y(CSIFile{idx}, CSIPath, LabelFile{idx}, LabelPath);
      end
    end
  else
    error('Select the same number of CSV and Y files.');
  end
elseif all(CSIFile ~= 0) && all(LabelFile ~= 0) % One file selected
  process_y(CSIFile, CSIPath, LabelFile, LabelPath);
elseif LabelFile ~= 0
  error('No converted CSI file (.csv) is selected');
else
  error('No labeling file (.y) is selected');
end
