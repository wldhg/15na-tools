import csv
import glob
import math
import numpy as np
import Config as conf

def readCSV(filePath):
  return np.asarray([
    [float(cell) for cell in line] for line in csv.reader(open(filePath, "r"))
  ])


def getWindows():
  # Read all csvs
  csi_csvs = sorted(glob.glob(conf.CSI_PATH))
  label_csvs = sorted(glob.glob(conf.LABEL_PATH))
  assert len(csi_csvs) == len(label_csvs), 'The number of CSVs do not match'

  ocsis = []
  olabels = []
  pps = None
  winCol = None
  winRow = None
  winSlideRow = None
  winRecogRow = None
  winAllRow = 0
  labelSum = [0] * (conf.ACTION_CNT + 1)

  # Read CSV files
  for i in range(len(csi_csvs)):
    print("Loading {} and {} ...".format(csi_csvs[i], label_csvs[i]))
    ocsi = readCSV(csi_csvs[i])
    olabel = readCSV(label_csvs[i])[:, 1]
    assert ocsi.shape[0] == olabel.shape[0], 'The rows of CSI & label are different'
    if pps == None:
      pps = np.where(ocsi[:, 0] == 1)[0][0]
      winCol = ocsi.shape[1] - 1
      winRow = math.floor(conf.WINDOW_SIZE * pps)
      winSlideRow = math.floor(conf.LEARN_SLIDE_SIZE * pps)
      winRecogRow = math.floor(conf.RECOGNITION_SIZE * pps)
      print(" - PPS determined: {}".format(pps))
      print(" - COL determined: {}".format(winCol))
      print(" - ROW determined: {}".format(winRow))
      print(" - SLIDE determined: {}".format(winSlideRow))
      print(" - RECOG determined: {}".format(winRecogRow))
    winAllRow = winAllRow + 1 + math.floor((ocsi.shape[0] - winRow) / winSlideRow)
    ocsis.append(ocsi)
    olabels.append(olabel)
  actCSI = np.empty([winAllRow, winRow, winCol])
  actLabel = np.empty([winAllRow, 1])
  actCursor = 0
  nonactCSI = np.empty([0, winRow, winCol])
  nonactCursor = 0
  if conf.USE_NOACTIVITY:
    nonactCSI = np.empty([winAllRow, winRow, winCol])
  print('{} windows may produced at maximum.'.format(winAllRow))

  # Really create window!
  for i in range(len(csi_csvs)):
    print("Creating windows from {} and {} ...".format(csi_csvs[i], label_csvs[i]))
    ocsi = ocsis[i]
    olabel = olabels[i]
    for j in range(1 + math.floor((ocsi.shape[0] - winRow) / winSlideRow)):
      startRow = j * winSlideRow
      partialLabelSum = np.zeros((conf.ACTION_CNT + 1), dtype=int)
      for k in range(startRow, startRow + winRow):
        labelPos = int(olabel[k])
        partialLabelSum[labelPos] = partialLabelSum[labelPos] + 1
      recogLabel = np.argmax((partialLabelSum - winRecogRow)[1:])
      if (partialLabelSum[recogLabel + 1] - winRecogRow >= 0) and (conf.NOACTIVITY_LABEL != (recogLabel + 1)):
        actCSI[actCursor, :, :] = ocsi[startRow:(startRow + winRow), 1:]
        if conf.EXCLUDE_NOACTIVITY:
          actLabel[actCursor] = recogLabel
          labelSum[recogLabel] = labelSum[recogLabel] + 1
        else:
          actLabel[actCursor] = recogLabel + 1
          labelSum[recogLabel + 1] = labelSum[recogLabel + 1] + 1
        actCursor = actCursor + 1
      elif conf.USE_NOACTIVITY and (
        conf.NOACTIVITY_AUTO or conf.NOACTIVITY_LABEL == recogLabel + 1):
        nonactCSI[nonactCursor, :, :] = ocsi[startRow:(startRow + winRow), 1:]
        nonactCursor = nonactCursor + 1
        labelSum[0] = labelSum[0] + 1
      elif conf.EXCLUDE_NOACTIVITY:
        pass

  # Remove some nonactivity windows
  labelConv = {}
  for i in range(int(conf.USE_NOACTIVITY), len(conf.LABEL) + 1):
    if i != conf.NOACTIVITY_LABEL:
      labelConv[i] = len(labelConv) + 1
      print("Windows for {} is {}.".format(
        conf.LABEL[i - 1],
        labelSum[i - conf.EXCLUDE_NOACTIVITY]
      ))
  if conf.USE_NOACTIVITY:
    print("Windows for NoAct is {}.".format(nonactCursor))
    noActivityCountMax = math.floor((actCursor / (len(conf.LABEL) - (not conf.NOACTIVITY_AUTO))) * 1.2) + 10
    nonactCSI = nonactCSI[:nonactCursor]
    if noActivityCountMax < nonactCursor:
      np.random.shuffle(nonactCSI)
      nonactCSI = nonactCSI[:noActivityCountMax]
      print("Windows for NoAct is reduced to {}.".format(noActivityCountMax))

  # Finalize CSIs
  print("Finally gathering windows...")
  fcsi = np.empty([nonactCSI.shape[0] + actCursor, winRow, winCol])
  flabel = np.empty([nonactCSI.shape[0] + actCursor, conf.ACTION_CNT])
  eye = np.eye(conf.ACTION_CNT)
  for i in range(actCursor):
    fcsi[i, :, :] = actCSI[i, :, :]
    flabel[i, :] = eye[labelConv[int(actLabel[i])]]
  if conf.USE_NOACTIVITY:
    for i in range(nonactCSI.shape[0]):
      fcsi[actCursor + i, :, :] = nonactCSI[i, :, :]
      flabel[actCursor + i, :] = eye[0]

  labelString = conf.LABEL
  if conf.USE_NOACTIVITY:
    labelString = ['NoAct'] + labelString
    if not conf.NOACTIVITY_AUTO:
      labelString.pop(conf.NOACTIVITY_LABEL)
  print("Label String Notice:", labelString)
  print("Shape Notice: [csi]", fcsi.shape, "[label]", flabel.shape)
  print("Completed!")

  return fcsi, flabel, [winRow, winCol]


if __name__ == "__main__":
  getWindows()
