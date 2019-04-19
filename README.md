# Syaa Tools

This repository includes codomain (for CSI data) maker, CSI(.dat) to CSV converter, and RNN learner for data.\
`prep-xy` directory is partially based on [ermongroup/Wifi_Activity_Recognition](https://github.com/ermongroup/Wifi_Activity_Recognition).

## **Overall Process**

1. Record CSI data with recording Y data using `make-y`.
2. Convert their raw data to learnable `.csv` data using `prep-xy`.
3. Do machine learning them using `learn-xy`.

## `make-y`

This makes codomain for csi data.

#### How to use

1. Install `node`.
2. Go `make-y` directory and enter `npm i`.
3. Enter `npm start` on `make-y` directory.
4. Instructions for the program will be shown up to the screen.

#### Caution

Start below two **simultaneously!**

-   Pressing `s` button on `make-y` program
-   Starting logging by launching `log_to_file` program

## `prep-xy`

This make proper csv files of CSI data (x) and Y (y).\
All results will be saved on the same directory of input file.

#### How to use

1. Launch MATLAB.
2. Add `prep-xy` directory and its subdirectory to the path.
3. Run `prep_x()` on command line and select raw CSI `.dat` file(s).
4. Run `prep_y()` on command line and select converted CSI (`.csv`) file(s) and raw y `.y` file(s).

#### Caution

On step 4 above, if you selected multiple `.csv` and `.y` files, the name of `.csv` files and `y` file must be matched following below rules.

-   *csi_(Name)**.csv*** `does be matched` with *(Name).**y***.
-   *(Name A)**.csv*** `does not be matched` with *(Name B).**y***.
-   *(Name)**.csv*** `does not be matched` with *(Name).**y***.


## `learn-xy`

This does learning of X and Y.\
**For how to use**, look [here](learn-xy/README.md).

## License

All the things are MIT license.
