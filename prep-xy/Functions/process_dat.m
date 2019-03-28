function ret = process_dat(fn, pn)
    raw_data = read_bf_file(strcat(pn, fn));
    
    % eliminate empty cell
    empty_cells = find(cellfun('isempty', raw_data));
    raw_data(empty_cells) = [];

    % Extract CSI information for each packet
    fprintf('Have CSI for %d packets\n', length(raw_data));

    % zeros(CSI data length, antenna, antenna, subcarriers (groupped by Intel 5300))
    csi = zeros(length(raw_data), raw_data{1}.Ntx, raw_data{1}.Nrx, 30);
    timestamp = zeros(1, length(raw_data));
    temp = [];
    fprintf('[1] Data space initialized\n');

    % Scaled into linear
    fprintf('[2] Scaling into linear\n');
    for pidx = 1:length(raw_data)
        csi(pidx,:,:,:) = get_scaled_csi(raw_data{pidx});
        timestamp(pidx) = (raw_data{pidx}.timestamp_low - raw_data{1}.timestamp_low) * 1.0e-6;
        if mod(pidx, 100) == 0 && pidx ~= 0
            if mod(pidx, 10000) == 0
                fprintf('*\n');
            else
                fprintf('.');
            end
        end
    end
    if mod(length(raw_data), 100) ~= 0
        fprintf('\n');
    end
    timestamp = timestamp';
    
    % File export
    fprintf('[3] Calculating amplitude & phase\n');
    csi_amp = permute(db(abs(squeeze(csi))), [2 3 4 1]);
    csi_phase = permute(angle(squeeze(csi)), [2 3 4 1]);
    
    fprintf('[4] Calibrating phase\n');
    cali_phase_counter = 1;
    for k = 1:size(csi_phase, 1)
        for m = 1:3
            for j = 1:size(csi_phase, 4)
                csi_phase_calibrated(k, m, :, j) = phase_calibration(csi_phase(k, m, :, j));
                if mod(cali_phase_counter, 900) == 0 && pidx ~= 0
                    if mod(cali_phase_counter, 90000) == 0
                        fprintf('*\n');
                    else
                        fprintf('.');
                    end
                end
                cali_phase_counter = cali_phase_counter + 1;
            end
        end
    end
    if mod(cali_phase_counter, 90000) ~= 0
        fprintf('\n');
    end

    fprintf('[5] Merging data\n');
    for pidx = 1:length(raw_data)
        temp = [temp;horzcat(reshape(squeeze(csi_amp(1,:,:,pidx))', [1, 90]), ...
                             reshape(squeeze(csi_phase_calibrated(1,:,:,pidx))', [1,90]), ...
                             reshape(squeeze(csi_amp(2,:,:,pidx))', [1, 90]), ...
                             reshape(squeeze(csi_phase_calibrated(2,:,:,pidx))', [1,90]), ...
                             reshape(squeeze(csi_amp(3,:,:,pidx))', [1, 90]), ...
                             reshape(squeeze(csi_phase_calibrated(3,:,:,pidx))', [1,90]))];
        if mod(pidx, 100) == 0 && pidx ~= 0
            if mod(pidx, 10000) == 0
                fprintf('*\n');
            else
                fprintf('.');
            end
        end
    end
    if mod(length(raw_data), 100) ~= 0
        fprintf('\n');
    end

    fprintf('[6] Saving CSV\n');
    dlmwrite([char(pn), char(fn), '.csv'], horzcat(timestamp, temp), 'delimiter', ',', 'precision', 10);
    fprintf('Successfully converted to CSV.\n');
end
