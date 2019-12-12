addpath(genpath('./functions/'));

% Configure
conf = inputdlg( ...
  {'Packets per seconds:', 'Select Tx antenna(s) [1|2|3]:', 'Select Rx antenna(s) [1|2|3]:', 'Process target [amp|phase|amphase]:'}, ...
  'Conversion Configuration', ...
  [1 35], ...
  {'200', '1', '1', 'amp'});

if isempty(conf)
  error('Conversion canceled.');
end

pps = str2double(conf{1});
if isnan(pps)
  error('PPS is wrong:' + conf{1});
else
  fprintf('[CONFIG] pps=%d\n\n', pps);
end

txSplit = arrayfun(@(s) str2double(s),split(conf{2}, ',')');
rxSplit = arrayfun(@(s) str2double(s),split(conf{3}, ',')');
if ~(all(~isnan(txSplit)) && all(~isnan(rxSplit)))
  error('Tx/Rx configuration is wrong.');
else
  fprintf('[CONFIG] txSplit\n');
  disp(txSplit);
  fprintf('[CONFIG] rxSplit\n');
  disp(rxSplit);
end

if strcmp(conf{4}, 'amp') == 1
  procAmp = true;
  procPhase = false;
  fprintf('[CONFIG] proc=amp\n\n');
elseif strcmp(conf{4}, 'phase') == 1
  procAmp = false;
  procPhase = true;
  fprintf('[CONFIG] proc=phase\n\n');
elseif strcmp(conf{4}, 'amphase') == 1
  procAmp = true;
  procPhase = true;
  fprintf('[CONFIG] proc=amp,phase\n\n');
else
  error('Wrong process target setting: ' + conf{4});
end

% Autoconfig filter configs
hampel_k = floor(pps * 0.09);
hampel_sigma = 3;
sgolay_order = 3 + floor(pps / 300);
sgolay_frame_amp = floor(pps * 0.09);
sgolay_frame_phase = floor(pps * 0.11);
if (mod(sgolay_frame_amp, 2) == 0)
  sgolay_frame_amp = sgolay_frame_amp + 1;
end
if (mod(sgolay_frame_phase, 2) == 0)
  sgolay_frame_phase = sgolay_frame_phase + 1;
end

% Select files
[File, Path] = uigetfile('*.dat','MultiSelect','on');

% Start processing
if isa(File, 'cell') % Multiple files selected
  for idx = 1:length(File)
    process_dat( ...
      File{idx}, Path, pps, txSplit, rxSplit, procAmp, procPhase, conf{4}, ...
      true, false, null, ...
      true, hampel_k, hampel_sigma, ...
      true, sgolay_order, sgolay_frame_amp, sgolay_frame_phase );
  end
elseif File ~= 0 % One file selected
  process_dat( ...
    File, Path, pps, txSplit, rxSplit, procAmp, procPhase, conf{4}, ...
    true, false, null, ...
    true, hampel_k, hampel_sigma, ...
    true, sgolay_order, sgolay_frame_amp, sgolay_frame_phase );
else
  error('No file is selected. Conversion canceled.');
end
