function ret = process_dat( ...
  fn, pn, pps, txSplit, rxSplit, procAmp, procPhase, procString, ...
  wannaFileSave, putData, redData, ...
  use_hampel, hampel_k, hampel_sigma, ...
  use_sgolay, sgolay_order, sgolay_framelen_amp, sgolay_framelen_phase )
fprintf('Starts to convert a DAT file!\n');

proc = 1;
if ~(putData)
  fprintf("[%d] Reading %s ... ", proc, fn);
  raw_data = read_bf_file(strcat(pn, fn));

  % Eliminate empty cell
  empty_cells = cellfun('isempty', raw_data);
  raw_data(empty_cells) = [];
else
  fprintf("[%d] Reading data ... ", proc);
  raw_data = redData;
end

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
  fprintf('[%d] Reshaping & filtering amplitude... ', proc);
  for t = 1:ltx
    for r = 1:lrx
      for ch = 1:30
        filtered_amp = interp1(timestamp, ...
          reshape(ocsi_amp(t, r, ch, :), [1, length(uni)]), interpolated_timestamp);
        if (use_hampel)
          filtered_amp = hampel(filtered_amp, hampel_k, hampel_sigma);
        end
        if (use_sgolay)
          filtered_amp = sgolayfilt(filtered_amp, sgolay_order, sgolay_framelen_amp);
        end
        csi_amp(t, r, ch, :) = filtered_amp;
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
  fprintf('[%d] Calibrating & filtering phase... ', proc);
  for k = 1:ltx
    for m = 1:lrx
      for ch = 1:30
        filtered_phase = interp1(timestamp, ocsi_phase(k, m, ch, :), interpolated_timestamp);
        if (use_hampel)
          filtered_phase = hampel(filtered_phase, hampel_k, hampel_sigma);
        end
        if (use_sgolay)
          filtered_phase = sgolayfilt(filtered_phase, sgolay_order, sgolay_framelen_phase);
        end
        csi_phase(k, m, ch, :) = filtered_phase;
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
if (wannaFileSave)
  fprintf('[%d] Final: Saving in CSV... ', proc);
  spath = [char(pn), 'csi_', char(strrep(fn, '.dat', '')), '_', num2str(pps), '_', num2str(ltx), 'x', num2str(lrx), '_', procString, '.csv'];
  dlmwrite(spath, horzcat(interpolated_timestamp', ret), 'delimiter', ',', 'precision', 8);
  sdir = dir(spath);
  fprintf('OK! (%d bytes)\n', sdir.bytes);
else
  fprintf('[%d] Final: Concatenating timestamp and csi... ', proc);
  ret = horzcat(interpolated_timestamp', ret);
  fprintf('OK!\n');
end
fprintf('Successfully converted to CSV.\n');
end
