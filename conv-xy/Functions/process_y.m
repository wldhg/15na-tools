function ret = process_y(CSVFile, CSVPath, YFile, YPath)
    fprintf('READ... ');
    csi = csvread(strcat(CSVPath, CSVFile));
    y_raw = csvread(strcat(YPath, YFile));

    fprintf('CONV... ');

    y = zeros(length(csi), 2);
    for idx = 1:length(csi)
        y(idx, :) = [csi(idx, 1) 0];
    end

    for idx = 1:size(y_raw, 1)
        for c_idx = 1:length(csi)
            if y(c_idx, 1) >= y_raw(idx, 2) && y(c_idx, 1) <= y_raw(idx, 3)
                y(c_idx, 2) = y_raw(idx, 1);
            end
        end
    end

    fprintf('SAVE... ');
    FileName = strrep(CSVFile, '.csv', '');
    FileName = strrep(FileName, 'csi_', '');
    dlmwrite([char(CSVPath), 'action_', char(FileName), '.csv'], y, 'delimiter', ',', 'precision', 8);
    fprintf('OK!\n');
end
