# Syaa Tools

This repository includes codomain (for CSI data) maker, CSI(.dat) to CSV converter, RNN learner for data, and data to video converter.\
`prep-xy` directory is partially based on [ermongroup/Wifi_Activity_Recognition](https://github.com/ermongroup/Wifi_Activity_Recognition).

## **Overall Process**

1. Record CSI data with recording Y data using `make-y`.
2. Convert their raw data to learnable `.csv` data using `prep-xy`.
3. Do machine learning them using `learn-xy`.
4. You can convert classification results to mp4 video using `video-xy`.

## How to use
Please look each directories' README.

#### Caution
- `video-xy` uses configurations and data from `learn-xy`.

## License

All the things are MIT license.
