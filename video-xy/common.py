### IMPORTS
# First Import
import os
import sys
sys.path.append('../learn-xy')

# Secondary Import
import CSV as csv
import Config as conf
import progressbar as pb
import numpy as np
import cv2

### PARAMETERS
# NOTE: {conf.VID_FPS * conf.VID_EXPAND} must be lower than {conf.PKT_HZ}
conf.VID_FPS = 30  # Video FPS
conf.VID_EXPAND = 4  # Expand 1 second of data to {conf.VID_EXPAND} seconds of video
conf.VID_NAME = "{0}-{1}.mp4"  # (fixed) File name scheme
conf.VID_CSIY_X = 480  # -y videos size (width)
conf.VID_CSIY_Y = 320  # -y videos size (height)
conf.VID_FONT = cv2.FONT_HERSHEY_SIMPLEX  # Video font
conf.VID_FONTSIZE = 3  # Video font size
conf.VID_THRESHOLD = 0.95  # Classification threshold
conf.VID_DELCUSTOMNA = False  # Delete custom NoActivity


### CONSTANTS
red = np.zeros((conf.VID_CSIY_Y, conf.VID_CSIY_X, 3), np.uint8)
red[:, :] = (66, 75, 244)
def getRed(): return red
green = np.zeros((conf.VID_CSIY_Y, conf.VID_CSIY_X, 3), np.uint8)
green[:, :] = (79, 255, 175)
def getGreen(): return green
def getFPS(): return conf.VID_FPS


### COMMON FUNCTIONS
def getNx(path):
    return np.array(csv.getFloatRawCSV(path))


def getNecessaryFrameNo(nx):
    return nx[nx.shape[0] - 1, 0] / conf.VID_EXPAND / conf.VID_FPS


def getNecessaryFrameIdx(nx):
    nxSec = np.copy(nx[:, 0])
    nxFinalSec = nx[nx.shape[0] - 1, 0]
    frameIter = 1
    frameInterval = 1 / conf.VID_EXPAND / conf.VID_FPS
    frameNo = [0]
    while frameIter * frameInterval < nxFinalSec:
        nrstIdx = (np.abs(nxSec - frameIter * frameInterval)).argmin()
        frameNo.append(frameNo[len(frameNo) - 1] + nrstIdx)
        nxSec = nxSec[nrstIdx:]
        frameIter += 1
    return frameNo


def saveVideo(name, frames):
    assert len(frames) > 0
    with pb.ProgressBar(max_value=len(frames)) as bar:
        videoFourcc = cv2.VideoWriter_fourcc(*'MP4V')
        videoSize = (frames[0].shape[1], frames[0].shape[0])
        videoOut = cv2.VideoWriter(
            name, videoFourcc, conf.VID_FPS, videoSize)
        for i in range(len(frames)):
            videoOut.write(frames[i])
            bar.update(i + 1)
        videoOut.release()
