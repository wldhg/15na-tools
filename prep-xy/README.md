# Syaa Tools - `prep-xy`

This make proper csv files of CSI data (x) and Y (y).\
All results will be saved on the same directory of input file.

### Prerequisites

-   MATLAB 2015 +

### How to use

1. Add `prep-xy` directory and its subdirectory to the path.
2. Run `prep_x()` on command line and select raw CSI `.dat` file(s).
3. Run `prep_y()` on command line and select converted CSI (`.csv`) file(s) and raw y `.y` file(s).

### Caution

On step 4 above, if you selected multiple `.csv` and `.y` files, the name of `.csv` files and `y` file must be matched following below rules.

-   _csi\_(Name)**.csv**_ `will be matched` with _(Name).**y**_.
-   _(Name A)**.csv**_ `does not be matched` with _(Name B).**y**_.
-   _(Name)**.csv**_ `does not be matched` with _(Name).**y**_.
