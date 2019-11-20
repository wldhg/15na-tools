# Cross Validation Learner Configuration

### Packet Details ###
WINDOW_SIZE = 0.6 # in seconds. A classification window size.
LEARN_SLIDE_SIZE = 0.04  # in seconds. Learning window slide length.
RECOGNITION_SIZE = 0.3  # in seconds. If an action continues more than this, the label of that window may be the action.

### Actions ###
LABEL = ['sitdown']  # This have to match with label number (starts from 1)
INCLUDE_NOACTIVITY = True  # Set "True" will include NoActivity windows in learning

### Learning Parameters ###
LEARNING_RATE = 0.002
EPOCH_CNT = 64
BATCH_SIZE = 256

### Learning Configurations ###
KFOLD = 2  # K of K-Fold
EVAL_FREQ = 2  # Validation frequency
CP_FREQ = 2048  # Checkpoint creation frequency. This must be a multiply of EVAL_FREQ.

### Path ###
CSV_DIRECTORY = 'Dataset'  # Directory contains 'csi_*.csv's and 'label_*.csv's

### FIXED VALUES ###
EXCLUDE_NOACTIVITY = not INCLUDE_NOACTIVITY
ACTION_CNT = len(LABEL) + INCLUDE_NOACTIVITY
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
