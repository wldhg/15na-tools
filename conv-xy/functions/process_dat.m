function process_dat(fn, pn, pps, txSplit, rxSplit, procAmp, procPhase, procString)
fprintf('Starts to convert a DAT file!\n');

proc = 1;
fprintf("[%d] Reading %s ... ", proc, fn);
raw_data = read_bf_file(strcat(pn, fn));

% Eliminate empty cell
empty_cells = cellfun('isempty', raw_data);
raw_data(empty_cells) = [];

% Extract CSI information for each packet
if ~isempty(raw_data)
  fprintf('OK! (%d pkts, %d x %d MIMO)\n', length(raw_data), raw_data{1}.Ntx, raw_data{1}.Nrx);
else
  fprintf('No Packet! Stopping.\n');
  return;
end

% Check Tx/Rx count
proc = proc + 1;
fprintf('[%d] Calculating Tx/Rx count... ', proc);
if (raw_data{1}.Ntx < max(txSplit) || raw_data{1}.Nrx < max(rxSplit))
  fprintf('Tx/Rx does not match. Stop these packets.\n');
  return;
end
ltx = length(txSplit);
lrx = length(rxSplit);
lrx30 = lrx * 30;
lpair = ltx * lrx;
fprintf('OK!\n');

% zeros(CSI data length, antenna, antenna, subcarriers (groupped by Intel 5300))
proc = proc + 1;
fprintf('[%d] Initializing data space... ', proc);
ocsi = zeros(length(raw_data), raw_data{1}.Ntx, raw_data{1}.Nrx, 30);
timestamp = zeros(length(raw_data), 1);
fprintf('OK!\n');

% Scaled into linear
proc = proc + 1;
fprintf('[%d] Scaling into linear... ', proc);
ocsi(1,:,:,:) = get_scaled_csi(raw_data{1});
zero_timestamp = raw_data{1}.timestamp_low;
addi_timestamp = 0;
timestamp(1) = 0;
for pidx = 2:length(raw_data)
  ocsi(pidx,:,:,:) = get_scaled_csi(raw_data{pidx});
  if raw_data{pidx}.timestamp_low < raw_data{pidx - 1}.timestamp_low
    % Timestamp Reset
    addi_timestamp = addi_timestamp + raw_data{pidx - 1}.timestamp_low - zero_timestamp;
    zero_timestamp = 0;
  end
  timestamp(pidx) = (raw_data{pidx}.timestamp_low - zero_timestamp + addi_timestamp) * 1.0e-6;
end
fprintf('OK! (%4f seconds)\n', timestamp(length(timestamp)));

% Consider uniqueness
proc = proc + 1;
fprintf('[%d] Consider uniqueness... ', proc);
[timestamp, uni] = unique(timestamp);
ocsi = ocsi(uni, :, :, :);
fprintf('OK!\n');

% Select tx/rx pairs -- Filter TR Pair in here
proc = proc + 1;
fprintf('[%d] Select Tx/Rx pairs... ', proc);
csi = zeros(length(uni), ltx, lrx, 30);
for txi = 1:ltx
  for rxi = 1:lrx
    csi(:, txi, rxi, :) = ocsi(:, txSplit(txi), rxSplit(rxi), :);
  end
end
interpolated_timestamp = 0:(1/pps):timestamp(length(timestamp));
lpkt = length(interpolated_timestamp);
fprintf('OK!\n');

% Convert to real values & preprocess (amp & phase) -- Filter Phase/Amp in here
if (procAmp)
  proc = proc + 1;
  fprintf('[%d] Permuting amplitude... ', proc);
  ocsi_amp = permute(db(abs(csi) + 1), [2 3 4 1]);
  csi_amp = zeros(ltx, lrx, 30, lpkt);
  fprintf('OK!\n');
  proc = proc + 1;
  fprintf('[%d] Applying Hampel filter to amplitude... ', proc);
  for t = 1:ltx
    for r = 1:lrx
      for ch = 1:30
        csi_amp(t, r, ch, :) = ...
          interp1(timestamp, hampel( ...
          reshape(ocsi_amp(t, r, ch, :), [1, length(uni)]), ...
          6, 1.6 ), ...
          interpolated_timestamp );
      end
    end
  end
  fprintf('OK!\n');
end
if (procPhase)
  proc = proc + 1;
  fprintf('[%d] Permuting phase... ', proc);
  ocsi_phase = permute(angle(csi), [2 3 4 1]);
  partial_phase = zeros(30, length(uni));
  csi_phase = zeros(ltx, lrx, 30, lpkt);
  fprintf('OK!\n');
  proc = proc + 1;
  fprintf('[%d] Calibrating phase... ', proc);
  for k = 1:ltx
    for m = 1:lrx
      for j = 1:length(uni)
        partial_phase(:, j) = phase_calibration(ocsi_phase(k, m, :, j));
      end
      for ch = 1:30
        csi_phase(k, m, ch, :) = interp1(timestamp, partial_phase(ch, :), interpolated_timestamp);
      end
    end
  end
  fprintf('OK!\n');
end

% Export to windows
proc = proc + 1;
fprintf('[%d] Merging into windows... ', proc);
ret = zeros(lpkt, 30 * (procAmp + procPhase) * lpair);
if (procPhase && procAmp)
  if (ltx == 1)
    for pidx = 1:lpkt
      ccAmp = reshape(squeeze(csi_amp(1, :, :, pidx))', [1, lrx30]);
      ccPhase = reshape(squeeze(csi_phase(1, :, :, pidx))', [1, lrx30]);
      ret(pidx, :) = horzcat(ccAmp, ccPhase);
    end
  elseif (ltx == 2)
    for pidx = 1:lpkt
      ccAmp = horzcat( ...
        reshape(squeeze(csi_amp(1, :, :, pidx))', [1, lrx30]), ...
        reshape(squeeze(csi_amp(2, :, :, pidx))', [1, lrx30]) );
      ccPhase = horzcat( ...
        reshape(squeeze(csi_phase(1, :, :, pidx))', [1, lrx30]), ...
        reshape(squeeze(csi_phase(2, :, :, pidx))', [1, lrx30]) );
      ret(pidx, :) = horzcat(ccAmp, ccPhase);
    end
  else
    for pidx = 1:lpkt
      ccAmp = horzcat( ...
        reshape(squeeze(csi_amp(1, :, :, pidx))', [1, lrx30]), ...
        reshape(squeeze(csi_amp(2, :, :, pidx))', [1, lrx30]), ...
        reshape(squeeze(csi_amp(3, :, :, pidx))', [1, lrx30]) );
      ccPhase = horzcat( ...
        reshape(squeeze(csi_phase(1, :, :, pidx))', [1, lrx30]), ...
        reshape(squeeze(csi_phase(2, :, :, pidx))', [1, lrx30]), ...
        reshape(squeeze(csi_phase(3, :, :, pidx))', [1, lrx30]) );
      ret(pidx, :) = horzcat(ccAmp, ccPhase);
    end
  end
elseif (procAmp)
  if (ltx == 1)
    for pidx = 1:lpkt
      ret(pidx, :) = reshape(squeeze(csi_amp(1, :, :, pidx))', [1, lrx30]);
    end
  elseif (ltx == 2)
    for pidx = 1:lpkt
      ret(pidx, :) = horzcat( ...
        reshape(squeeze(csi_amp(1, :, :, pidx))', [1, lrx30]), ...
        reshape(squeeze(csi_amp(2, :, :, pidx))', [1, lrx30]) );
    end
  else
    for pidx = 1:lpkt
      ret(pidx, :) = horzcat( ...
        reshape(squeeze(csi_amp(1, :, :, pidx))', [1, lrx30]), ...
        reshape(squeeze(csi_amp(2, :, :, pidx))', [1, lrx30]), ...
        reshape(squeeze(csi_amp(3, :, :, pidx))', [1, lrx30]) );
    end
  end
elseif (procPhase)
  if (ltx == 1)
    for pidx = 1:lpkt
      ret(pidx, :) = reshape(squeeze(csi_phase(1, :, :, pidx))', [1, lrx30]);
    end
  elseif (ltx == 2)
    for pidx = 1:lpkt
      ret(pidx, :) = horzcat( ...
        reshape(squeeze(csi_phase(1, :, :, pidx))', [1, lrx30]), ...
        reshape(squeeze(csi_phase(2, :, :, pidx))', [1, lrx30]) );
    end
  else
    for pidx = 1:lpkt
      ret(pidx, :) = horzcat( ...
        reshape(squeeze(csi_phase(1, :, :, pidx))', [1, lrx30]), ...
        reshape(squeeze(csi_phase(2, :, :, pidx))', [1, lrx30]), ...
        reshape(squeeze(csi_phase(3, :, :, pidx))', [1, lrx30]) );
    end
  end
end
fprintf('OK!\n');

% Save CSV
proc = proc + 1;
fprintf('[%d] Saving in CSV... ', proc);
spath = [char(pn), 'csi_', char(strrep(fn, '.dat', '')), '_', num2str(pps), '_', num2str(ltx), 'x', num2str(lrx), '_', procString, '.csv'];
dlmwrite(spath, horzcat(interpolated_timestamp', ret), 'delimiter', ',', 'precision', 8);
fprintf('OK! (%d bytes)\n', dir(spath).bytes);
fprintf('Successfully converted to CSV.\n');
end
