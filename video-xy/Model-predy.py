import gc
import sys
import cv2
import progressbar as pb
import numpy as np
import keras.optimizers as ko
import keras.models as km
import matplotlib.pyplot as plt
from io import BytesIO
from common import *


# Define common function
def createGraph(scores):
    pltLegend = []
    pltFigure = plt.figure()
    pltImage = BytesIO()
    plt.bar(conf.ACTIONS, scores, figure=pltFigure)
    plt.ylabel('Prediction Accuracy', figure=pltFigure)
    plt.ylim(0, 1)
    pltFigure.savefig(pltImage, format='png')
    plt.close(pltFigure)
    pltImage.seek(0)
    cvImage = cv2.imdecode(np.asarray(
        bytearray(pltImage.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
    return cvImage


# Load CSV & Calculate necessary frames
assert len(sys.argv) == 4
print("[1/7] Reading & Converting CSV ( " + sys.argv[1] + " ) ...")
nx = getNx(sys.argv[1])
mx, my = csv.mergeCSVOfAction(sys.argv[1])
mx = mx.reshape(len(mx), conf.WINDOW_SIZE, conf.PKT_COLUMNS)
print("[2/7] Calculating necessary frames...")
frameIdx = getNecessaryFrameIdx(nx)
frameLen = len(frameIdx)

# Load keras model and classify each slide
print("[3/7] Load Keras model...")
adam = ko.Adam(lr=conf.LEARNING_RATE, amsgrad=True)
modelPropRaw = open(sys.argv[3], 'r')
if 'json' in modelProp:
    model = km.model_from_json(modelPropRaw)
else:
    model = km.model_from_yaml(modelPropRaw)
model.load_weights(sys.argv[2])
model.compile(loss="categorical_crossentropy",
              optimizer=adam, metrics=["accuracy"])
print("[4/7] Classify each slides...")
scores = model.predict(mx)
if conf.USE_NOACTIVITY == True:
    scores = scores[:, 1:]
elif conf.USE_CUSTOM_NOACTIVITY == True and conf.VID_DELCUSTOMNA == True:
    scores = np.delete(scores, conf.CUSTOM_NOACTIVITY_NO, 0)

# Calculate frame-prediction matches
print("[5/7] Calculating frame-prediction matchings...")
ny = []
frameMatching = []
lastFrame = -1
for fn in frameIdx:
    if fn < conf.WINDOW_SIZE:
        frameMatching.append(-1)
    elif nx.shape[0] - fn - 1 < conf.WINDOW_SIZE:
        frameMatching.append(lastFrame)
    else:
        frameMatching.append(int((fn - conf.WINDOW_SIZE) / conf.SLIDE_SIZE))
for sc in scores:
    maxIdx = np.array(sc).argmax()
    if sc[maxIdx] >= conf.VID_THRESHOLD:
        ny.append(maxIdx)
    else:
        ny.append(-1)

# Calculate graphs
print("[6/7] Creating graphs and color pages...")
clfFrames = []
predFrames = []
scoreGraphs = []
barIdx = 0
ebgImage = createGraph(np.zeros(conf.N_VALID_CLASSES))
for s in scores:
    scoreGraphs.append(createGraph(s))
with pb.ProgressBar(max_value=frameLen) as bar:
    for p in frameMatching:
        if p == -1 or ny[p] == -1:
            clfFrames.append(getRed())
        else:
            colorFrame = np.copy(getGreen())
            cv2.putText(
                colorFrame,
                conf.ACTIONS[int(ny[p])],
                (30, conf.VID_CSIY_Y - 15 * conf.VID_FONTSIZE),
                conf.VID_FONT,
                conf.VID_FONTSIZE,
                (0, 0, 0),
                10
            )
            clfFrames.append(colorFrame)
        if p == -1:
            predFrames.append(ebgImage)
        else:
            predFrames.append(scoreGraphs[p])
        barIdx += 1
        bar.update(barIdx)

# Save as mp4 video
predVideoName = conf.VID_NAME.format(
    sys.argv[1][:sys.argv[1].index('.')], 'pred')
clfVideoName = conf.VID_NAME.format(
    sys.argv[1][:sys.argv[1].index('.')], 'clfy')
print("[7/7] Saving in " + predVideoName + " and " + clfVideoName + " ...")
saveVideo(predVideoName, predFrames)
saveVideo(clfVideoName, clfFrames)
