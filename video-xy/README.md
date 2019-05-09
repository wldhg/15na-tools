# 15na Tools - `video-y`

This tool converts your model & input to video.

### Requirements

-   All requirements of `learn-xy`
-   Python packages: `matplotlib`, `progressbar2`, `opencv`

### How to use

First you should change parameters in `common.py`.\
In below ways, you can also use equally-named Jupyter Notebook files.

#### To convert CSI amplitude data to video

```bash
$ python CSI-amp.py [CSV file of CSI from prep-xy]
```

#### To convert CSI amplitude difference from `NoActivity` to video

This will extract average CSI value of 'NoActivity' from same CSI csv file.\
You should specify begining and ending time of 'NoActivity' in seconds.

```bash
$ python CSI-amp-diff.py [CSV file of CSI from prep-xy] [time of the start of NoActivity] [time of the end of NoActivity]
```

#### To convert CSI phase data to video

```bash
$ python CSI-phase.py [CSV file of CSI from prep-xy]
```

#### To convert Original Y (manually-labeled) data to video

```bash
$ python CSI-y.py [CSV file of Y from prep-xy]
```

#### To convert Classified Y and prediction (model-labeled) data to video

```bash
$ python Model-predy.py [CSV file of CSI from prep-xy] [.h5 model] [.json or .yml model properties file]
```
