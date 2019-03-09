function ret = process_dat(fn, pn)
    raw_data = read_bf_file(strcat(pn, fn))
    
    % eliminate empty cell
    empty_cells = find(cellfun('isempty', raw_data));
    raw_data(empty_cells) = [];

    % Extract CSI information for each packet
    fprintf('Have CSI for %d packets\n', length(raw_data))

    % zeros(CSI data length, antenna, antenna, subcarriers (groupped by Intel 5300))
    csi = zeros(length(raw_data), raw_data{0}.Ntx, raw_data{0}.Nrx, 30)
    timestamp = zeros(1, length(raw_data))
    temp = []

    % Scaled into linear
    for pidx = 1:length(raw_data)
        csi(pidx,:,:,:) = get_scaled_csi(raw_data{pidx})
        timestamp(pidx) = raw_data{pidx}.timestamp_low * 1.0e-6
    end
    timestamp = timestamp'

    % File export
    csi_amp = permute(db(abs(squeeze(csi))), [2 3 4 1])
    csi_phase = permute(angle(squeeze(csi)), [2 3 4 1])
    
    for k = 1:size(csi_phase, 1)
        for m = 1:3
            for j = 1:size(csi_phase, 4)
                csi_phase_calibrated(k, m, :, j) = phase_calibration(csi_phase(k, m, :, j))
            end
        end
    end

    for pidx = 1:length(raw_data)
        temp = [temp;horzcat(reshape(squeeze(csi_amp(1,:,:,pidx))', [1, 90]), ...
                             reshape(squeeze(csi_phase_calibrated(1,:,:,pidx))', [1,90]), ...
                             reshape(squeeze(csi_amp(2,:,:,pidx))', [1, 90]), ...
                             reshape(squeeze(csi_phase_calibrated(2,:,:,pidx))', [1,90]), ...
                             reshape(squeeze(csi_amp(3,:,:,pidx))', [1, 90]), ...
                             reshape(squeeze(csi_phase_calibrated(3,:,:,pidx))', [1,90]))]
    end

    csvwrite([char(pn), char(fn), '.csv'], horzcat(timestamp, temp))
end
