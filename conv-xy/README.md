# 15na Tools - `conv-xy`

CSI `.dat` to CSV / Labeling `.y` to CSV conversion tool.

All results will be saved on the same directory of input files.

### Requirement

-   MATLAB R2015b or later

### How To Use

1. Add this `conv-xy` directory and its subdirectory to the MATLAB path.
2. Run `conv_x` and select CSI (`.dat`) file(s).
3. Execute `conv_y` and select converted CSI (`.csv`) file(s) and a labeling (`.y`) file.

### Post Script

You may enter "packets per seconds" when you try to convert `.dat` to `.csv`.\
This pps information is used to interpolate packet intervals.
