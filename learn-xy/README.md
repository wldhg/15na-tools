# POSCA Tools - `learn-xy`

### How to use

1. First, make directory named `Dataset` in `learn-xy` directory.
2. Modify `ACTIONS` of `Config.py`. You can modify other parameters now. If you want to change some parameters after this step, you must restart from step 3.
3. Put the source csv files into `Dataset` directory. Naming scheme is as below.
   If you put `['A', 'B']` in `ACTIONS`, the name of CSI data csv will be `csi_A...csv` and of Y data csv will be `action_A_...csv`.
   The important thing is that `...` part must be same. That is, `csi_A_asdf222.csv` will be matched with `action_A_asdf222.csv`.
4. Run `Keras.py`.
5. **???** ← This is what machine learning does.
6. After this, `Output_LR..._...` directory may be created and keras checkpoint file may be in there.
7. Profit!

### What can I do after this process?

You can do everything using your model and weight values. Copy `model.h5`, `model.yml` in output directory to everywhere you want to use your model. Enjoy it!
