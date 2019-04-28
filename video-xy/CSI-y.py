import gc
import sys
import cv2
import progressbar as pb
import numpy as np
from io import BytesIO
from common import *

if __name__ == "__main__":
    # Load CSV & Calculate necessary frames
    assert len(sys.argv) == 2
    print("[1/4] Loading CSV ( " + sys.argv[1] + " ) ...")
    nx = getNx(sys.argv[1])
    print("[2/4] Calculating necessary frames...")
    frameIdx = getNecessaryFrameIdx(nx)
    frameLen = len(frameIdx)

    # Calculate graphs
    print("[3/4] Creating colored y images...")
    frames = []
    barIdx = 0
    with pb.ProgressBar(max_value=frameLen) as bar:
        for p in frameIdx:
            if nx[p, 1] == 0:
                frames.append(getRed())
            else:
                frame = np.copy(getGreen())
                cv2.putText(
                    frame,
                    conf.ACTIONS[int(nx[p, 1] - 1)],
                    (30, conf.VID_CSIY_Y - 15 * conf.VID_FONTSIZE),
                    conf.VID_FONT,
                    conf.VID_FONTSIZE,
                    (0, 0, 0),
                    10
                )
                frames.append(frame)
            barIdx += 1
            bar.update(barIdx)

    # Save as mp4 video
    videoName = conf.VID_NAME.format(
        sys.argv[1][:sys.argv[1].index('.')], 'y')
    print("[4/4] Saving in " + videoName + " ...")
    saveVideo(videoName, frames)
