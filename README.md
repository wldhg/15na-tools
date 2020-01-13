# 15na Tools

Useful tools for CSI motion model making, works with [D. Halperin's CSITool](https://github.com/dhalperi/linux-80211n-csitool).

This toolset includes...

- `exam-x` : CSI analysis scripts
- `label-y` : CSI labeling tool
- `conv-xy` : CSI label file (`.y`) to CSV converter
- `conv-xy` : CSI file (`.dat`) to CSV Converter
- `train-xy` : Machine learning Jupyter notebooks
- `video-xy` : CSI CSV to mp4 visualization tool

## Overall Process

1. *(Optional)* Analyze each motions and data using `exam-x`.
2. Label recorded CSI data using tool in `label-y`.
3. Convert the CSI data to learnable `.csv` data using the `conv_x` tool in `conv-xy`.
4. Convert the label data to learnable `.csv` data using the `conv_y` tool in `conv-xy`.
5. Do machine learning them using notebooks in `train-xy`.
6. *(Optional)* You can convert the classification results, the CSI CSVs to mp4 video using tools in `video-xy`.

## How To Use

Please look each directories' README file.

## License

All the things are licensed under [MIT license](./LICENSE.md).

`conv-xy` directory is partially based on [ermongroup/Wifi_Activity_Recognition](https://github.com/ermongroup/Wifi_Activity_Recognition). Their license and copyright is included in [LICENSE.md](./LICENSE.md).
