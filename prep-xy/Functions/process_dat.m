function ret = process_dat(fn, pn)
    raw_data = read_bf_file(strcat(pn, fn));

    % eliminate empty cell
    empty_cells = find(cellfun('isempty', raw_data));
    raw_data(empty_cells) = [];

    % Extract CSI information for each packet
    fprintf('Have CSI for %d packets\n', length(raw_data));

    if length(raw_data) > 0
        fprintf(raw_data{1}.Ntx + "x" + raw_data{1}.Nrx + " MIMO log found.\n");
    end
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
                fprintf('*' + string(pidx / 1000) + 'k\n');
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
    csi_amp = permute(db(abs(csi) + 1), [2 3 4 1]);
    csi_phase = permute(angle(csi), [2 3 4 1]);

    fprintf('[4] Calibrating phase\n');
    cali_phase_counter = 1;
    cali_phase_counter_standard_100 = raw_data{1}.Ntx * raw_data{1}.Nrx * 100;
    cali_phase_counter_standard_1000 = cali_phase_counter_standard_100 * 10;
    cali_phase_counter_standard_10000 = cali_phase_counter_standard_100 * 100;
    for k = 1:raw_data{1}.Ntx
        for m = 1:raw_data{1}.Nrx
            for j = 1:length(raw_data)
                csi_phase_calibrated(k, m, :, j) = phase_calibration(csi_phase(k, m, :, j));
                if mod(cali_phase_counter, cali_phase_counter_standard_100) == 0 && pidx ~= 0
                    if mod(cali_phase_counter, cali_phase_counter_standard_10000) == 0
                        fprintf('*' + string(cali_phase_counter / cali_phase_counter_standard_1000) + 'k\n');
                    else
                        fprintf('.');
                    end
                end
                cali_phase_counter = cali_phase_counter + 1;
            end
        end
    end
    if mod(cali_phase_counter, cali_phase_counter_standard_10000) ~= 0
        fprintf('\n');
    end

    fprintf('[5] Merging data\n');
    for pidx = 1:length(raw_data)
        catenAmp = reshape(squeeze(csi_amp(1,:,:,pidx))', [1, 90]);
        catenPhase = reshape(squeeze(csi_phase_calibrated(1,:,:,pidx))', [1, 90]);
        if raw_data{1}.Ntx > 2
            for ntx = 2:raw_data{1}.Ntx
                catenAmp = horzcat(catenAmp, reshape(squeeze(csi_amp(ntx,:,:,pidx))', [1, 90]));
                catenPhase = horzcat(catenPhase, reshape(squeeze(csi_phase_calibrated(ntx,:,:,pidx))', [1, 90]));
            end
        end
        temp = [temp;horzcat(catenAmp, catenPhase)];
        if mod(pidx, 100) == 0 && pidx ~= 0
            if mod(pidx, 10000) == 0
                fprintf('*' + string(pidx / 1000) + 'k\n');
            else
                fprintf('.');
            end
        end
    end
    if mod(length(raw_data), 100) ~= 0
        fprintf('\n');
    end

    fprintf('[6] Saving CSV\n');
    fnWOdat = sttrep(fn, '.dat', '');
    dlmwrite([char(pn), 'csi_', char(fnWOdat), '.csv'], horzcat(timestamp, temp), 'delimiter', ',', 'precision', 10);
    fprintf('Successfully converted to CSV.\n');
end
