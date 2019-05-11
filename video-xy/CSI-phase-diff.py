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
    assert len(sys.argv) == 4
    avgBeginTime = float(sys.argv[2])
    avgEndTime = float(sys.argv[3])
    print("[1/5] Loading CSV ( " + sys.argv[1] + " ) ...")
    nx = getNx(sys.argv[1])
    print("[2/5] Calculating necessary frames...")
    frameIdx = getNecessaryFrameIdx(nx)
    frameLen = len(frameIdx)

    # Calculate avarage CSI and differences
    print("[3/5] Calculating average CSI...")
    cutNx = None
    beginIdx = 0
    for idx, row in enumerate(nx):
        if row[0] >= avgBeginTime:
            beginIdx = idx
            break
    for idx, row in reversed(list(enumerate(nx))):
        if row[0] < avgEndTime:
            cutNx = nx[beginIdx:idx, :]
            break
    avgPhase = np.mean(cutNx, axis=0)
    print("[4/5] Calculating differences...")
    diffNx = np.copy(nx) - avgPhase

    # Calculate graphs
    print("[5/5] Creating graphs and converting to cv format...")
    tr = int((nx.shape[1] - 1) / 60)
    for i in range(0, tr):
        frames = []
        barIdx = 0
        gc.collect()
        print("  -- Processing " + str(i + 1) + " th Tx-Rx Pair...")
        with pb.ProgressBar(max_value=frameLen) as bar:
            for p in frameIdx:
                pltLegend = []
                pltFigure = plt.figure()
                pltImage = BytesIO()
                pltLegend.append(str(i + 1) + 'TRP')
                plt.plot(
                    diffNx[p, (tr * 30 + 1 + 30 * i):(tr * 30 + 31 + 30 * i)],
                    color=('C' + str(i)),
                    figure=pltFigure
                )
                plt.xlabel('Subcarriers Group', figure=pltFigure)
                plt.ylabel('Phase Shift Diff [db]', figure=pltFigure)
                pltFigure.legend(pltLegend)
                plt.ylim(-10, 10)
                pltFigure.savefig(pltImage, format='png')
                plt.close(pltFigure)
                del pltFigure
                del pltLegend
                pltImage.seek(0)
                cvImage = cv2.imdecode(np.asarray(
                    bytearray(pltImage.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
                frames.append(cvImage)
                barIdx += 1
                bar.update(barIdx)
        # Save as mp4 video
        videoName = conf.VID_NAME.format(
            sys.argv[1][:sys.argv[1].index('.')], "phasediff-" + str(i + 1))
        print("  -- Saving in " + videoName + " ...")
        saveVideo(videoName, frames)
        print("  -- Delete old data...")
        del frames
    print("Finished!")
