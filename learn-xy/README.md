# 15na Tools - `learn-xy`

CNN learning scripts

### Required version & Packages

This works on **Python 3.6**

-   `keras` or `keras-gpu`
-   `numpy`
-   `scikit-learn`
-   `progressbar2`
-   `jupyter notebook`

### How to use

1. First, make directory named `Dataset` in `learn-xy` directory.
2. Modify `ACTIONS` of `Config.py`. You can modify other parameters now. If you want to change some parameters after this step, you must restart from step 3.
3. Put the source csv files into `Dataset` directory. Naming scheme is as below.
   If you put `['A', 'B']` in `SOURCES`, the name of CSI data csv will be `csi_A...csv` and of Y data csv will be `action_A_...csv`.
   The important thing is that `...` part must be same. That is, `csi_A_asdf222.csv` will be matched with `action_A_asdf222.csv`.
4. Run `Run_*.ipynb`.
5. **???** ← This is what machine learning does.
6. After this, `Output_LR..._...` directory may be created and keras checkpoint file may be in there.
7. Also, `model.h5`, `model.yml`, `model.json` will be in there.
8. **Profit!** Use these in your way.

### What can I do after this process?

You can do everything using your model. Enjoy it!

### About DenseNet Implementation

DenseNet implementation was made at [here](https://github.com/cmasch/densenet).
