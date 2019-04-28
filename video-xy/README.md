# Syaa Tools - `video-y`

This tool converts your model & input to video.

### Requirements

- All requirements of `learn-xy`
- Python packages: `matplotlib`, `progressbar2`, `opencv`

### How to use

First you should change parameters in `common.py`.

To convert CSI amplitude data to video,
```bash
$ python CSI-amp.py [CSV file of CSI from prep-xy]
```

To convert CSI phase data to video,
```bash
$ python CSI-phase.py [CSV file of CSI from prep-xy]
```

To convert Original Y (manually-labeled) data to video,
```bash
$ python CSI-y.py [CSV file of Y from prep-xy]
```

To convert Classified Y and prediction (model-labeled) data to video,
```bash
$ python Model-predy.py [CSV file of CSI from prep-xy] [.h5 model] [.json or .yml model properties file]
```

Or you can use Jupyter Notebook files.
