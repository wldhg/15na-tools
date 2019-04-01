# POSCA Tools

This repository includes codomain (for CSI data) maker, CSI(.dat) to CSV converter, and RNN learner for data.
`prep-xy` directory is partially based on [ermongroup's WAR](https://github.com/ermongroup/Wifi_Activity_Recognition).

## Overall Process

1. Record CSI data with running `make-y`.
2. Convert their raw data to learnable `.csv` data using `prep-xy`.
3. Do learn them using `learn-xy`.

## `make-y`

This makes codomain for csi data.

#### How to use

1. Install `node`.
2. Enter `npm i` and `npm start` on `make-y` directory.
3. Instructions for this program will be shown up to the screen.

#### Caution

Start these thing simultaneously!

-   Press `s` button on `make-y` program
-   Start logging using `log_to_file` program

## `prep-xy`

This make proper csv files of CSI data (x) and Y (y).
All results will be saved on the same directory of input file.

#### How to use

1. Run MATLAB.
2. Add `prep-xy` directory to path.
3. Run `prep_x()` on command line and select raw CSI `.dat` file.
4. Run `prep_y()` on command line and select converted CSI (`.csv`) file and raw y `.y` file.

## `learn-xy`

This does learning of X and Y.
**For how to use**, look [here](learn-xy/README.md).
