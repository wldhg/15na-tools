import gc
import sys
import cv2
import progressbar as pb
import matplotlib.pyplot as plt
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
    print("[3/4] Creating graphs and converting to cv format...")
    frames = []
    barIdx = 0
    with pb.ProgressBar(max_value=frameLen) as bar:
        for p in frameIdx:
            pltLegend = []
            pltFigure = plt.figure()
            pltImage = BytesIO()
            for i in range(0, int((nx.shape[1] - 1) / 60)):
                pltLegend.append(str(i + 1) + 'TR')
                plt.plot(nx[p, (1 + 30 * i):(31 + 30 * i)], figure=pltFigure)
                plt.xlabel('Subcarriers Group', figure=pltFigure)
                plt.ylabel('Amplitude CSI [db]', figure=pltFigure)
            pltFigure.legend(pltLegend)
            plt.ylim(0, 30)
            pltFigure.savefig(pltImage, format='png')
            plt.close(pltFigure)
            pltImage.seek(0)
            cvImage = cv2.imdecode(np.asarray(
                bytearray(pltImage.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
            frames.append(cvImage)
            barIdx += 1
            bar.update(barIdx)

    # Save as mp4 video
    videoName = conf.VID_NAME.format(
        sys.argv[1][:sys.argv[1].index('.')], 'amplitude')
    print("[4/4] Saving in " + videoName + " ...")
    saveVideo(videoName, frames)
