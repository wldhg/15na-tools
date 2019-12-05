# Cross Validation Learner Configuration

### Packet Details ###
# A classification window size in seconds.
WINDOW_SIZE = 0.6
# Learning window slide length in seconds
LEARN_SLIDE_SIZE = 0.005
# In seconds. If an action continues more than this,
# the label of that window may be the action.
RECOGNITION_SIZE = 0.5

### Actions ###
# This have to match with label number (starts from 1)
LABEL = ['noise', 'fall', 'floor', 'walk_a', 'walk_b', 'lay', 'wake']

### No Activity (Noise) ###
# Set this "auto" makes NoActivity windows to be included automatically.
# Otherwise, write NoActivity's label, which is one of LABEL array.
# If don't use no activity window, set this None.
NOACTIVITY = 'noise'
# Set this None make training include all noises.
# Or set this to a float number value to set the ratio of noactivity window
# as "AVERAGE COUNT OF WINDOWS OF ALL ACTIVITY LABELS" * NONACTIVITY_RATIO.
NOACTIVITY_RATIO = 9.4

### Learning Parameters ###
LEARNING_RATE = 0.002
EPOCH_CNT = 32
BATCH_SIZE = 512
KFOLD = 10  # K of K-Fold

### Path ###
# Directory contains 'csi_*.csv's and 'label_*.csv's
CSV_DIRECTORY = 'Dataset'

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
LABEL_PATH = CSV_DIRECTORY + "/label_*.csv"
OUTPUT_DIR = "./Output_{0}_LR{1}_B{2}_K{3}/".format(
  "{0}", LEARNING_RATE, BATCH_SIZE, KFOLD,
)
LOG_DIR = "./Log_{0}_LR{1}_B{2}_K{3}/".format(
  "{0}", LEARNING_RATE, BATCH_SIZE, KFOLD,
)
