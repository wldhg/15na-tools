# 15na Tools - `train-xy`

Machine learning Jupyter notebooks

### Requirements

This works on **Python 3**

- `tensorflow` or `tensorflow-gpu` 2.0 or later
- `numpy`
- `scikit-learn`
- `jupyter notebook`
- `tensorboard`

### How To Use

1. Modify parameters of `Config.py`.
2. Put the source csv files into `Dataset` directory.\
   All *CSI* csvs must be named as `csi_~.csv` and the corresponding *label* csvs should be `label_~.csv`.\
   If you used `conv-xy` tool, the naming scheme may already applied.
3. Run `[MODEL].ipynb`.
4. After learning, `Output_LR..._...` directory may be created and keras checkpoint file may be in there.
5. Also, `model.h5`, `model.yml`, `model.json` will be in there.
6. **Profit!** Use these in your way.

### Information

- I used `Double_LSTM` model.
- Some recent papers of Wi-Fi HAR used CNN, but my CNN model is not effective yet.
- If you found any better model, PR is always open.
