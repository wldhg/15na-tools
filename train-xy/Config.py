# Cross Validation Learner Configuration

### Packet Details ###
WINDOW_SIZE = 0.6 # in seconds. A classification window size.
LEARN_SLIDE_SIZE = 0.005  # in seconds. Learning window slide length.
RECOGNITION_SIZE = 0.5  # in seconds. If an action continues more than this, the label of that window may be the action.

### Actions ###
# This have to match with label number (starts from 1)
LABEL = ['fall_a', 'fall_b', 'fall_c', 'fall_d', 'noise', 'lay_static']

### No Activity (Noise) ###
# Set this "auto" makes NoActivity windows to be included automatically.
# Otherwise, write NoActivity's label, which is one of LABEL array.
# If don't use no activity window, set this None.
NOACTIVITY = 'noise'

### Learning Parameters ###
LEARNING_RATE = 0.002
EPOCH_CNT = 64
BATCH_SIZE = 256

### Learning Configurations ###
KFOLD = 5  # K of K-Fold
EVAL_FREQ = 2  # Validation frequency
CP_FREQ = 2048  # Checkpoint creation frequency. This must be a multiply of EVAL_FREQ.

### Path ###
CSV_DIRECTORY = 'Dataset'  # Directory contains 'csi_*.csv's and 'label_*.csv's

### FIXED VALUES ###
USE_NOACTIVITY = None
NOACTIVITY_LABEL = 0
if NOACTIVITY == None:
  USE_NOACTIVITY = False
else:
  USE_NOACTIVITY = True
  if NOACTIVITY != 'auto':
    NOACTIVITY_LABEL = LABEL.index(NOACTIVITY) + 1
EXCLUDE_NOACTIVITY = not USE_NOACTIVITY
NOACTIVITY_AUTO = NOACTIVITY_LABEL == 0
ACTION_CNT = len(LABEL) + NOACTIVITY_AUTO
CSI_PATH = CSV_DIRECTORY + "/csi_*.csv"
# CSI_PICKLE = CSV_DIRECTORY + "/csi.pckl"  # Not used yet
LABEL_PATH = CSV_DIRECTORY + "/label_*.csv"
# LABEL_PICKLE = CSV_DIRECTORY + "/label.pckl"  # Not used yet
OUTPUT_DIR = "./Output_LR{0}_B{1}_K{2}_CP{3}/".format(
  LEARNING_RATE, BATCH_SIZE, KFOLD, CP_FREQ
)
LOG_DIR = "./Log_LR{0}_B{1}_K{2}_CP{3}/".format(
  LEARNING_RATE, BATCH_SIZE, KFOLD, CP_FREQ
)
