function ret = process_y(CSVFile, CSVPath, YFile, YPath)
    fprintf('Reading CSV and Y file...\n');
    csi = csvread(strcat(CSVPath, CSVFile));
    y_raw = csvread(strcat(YPath, YFile));

    fprintf('Initializing converted y values...\n');
    y = zeros(length(csi), 2);
    for idx = 1:length(csi)
        y(idx, :) = [csi(idx, 1) 0];
    end

    fprintf('Converting y values...\n');
    c_idx_saved = 1;
    for idx = 1:size(y_raw, 1)
        for c_idx = c_idx_saved:length(csi)
            if y(c_idx, 1) >= y_raw(idx, 2)
                c_idx_saved = c_idx;
                break
            end
        end
        for c_idx = c_idx_saved:length(csi)
            if y(c_idx, 1) <= y_raw(idx, 3)
                y(c_idx, 2) = y_raw(idx, 1);
            else
                c_idx_saved = c_idx;
                break
            end
        end
    end
    fprintf('Converting finished!\n');

    fprintf('Saving converted file...\n');
    YFileWOy = strrep(YFile, '.y', '')
    dlmwrite([char(YPath), 'action_', char(YFileWOy), '.csv'], y, 'delimiter', ',', 'precision', 10);
    fprintf('Successfully converted y to csv.\n');
end
