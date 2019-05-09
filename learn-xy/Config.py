# Cross Validation Learner Configuration

### Packet Details ###
PKT_HZ = 4700  # pps (packets-per-second)
WINDOW_SIZE = int(PKT_HZ * 0.4)  # How many packets in one detection; depends on pps and the length of time of the action
SLIDE_SIZE = int(WINDOW_SIZE / 10)  # Packet interval in learning (Window-making interval)
THRESHOLD = 80  # If specific action continues after [WINDOW_SIZE * THRESHOLD / 100], that window will be recognized as that action
MULTIPLE_INPUT = 3  # The number of Tx of MIMO
MULTIPLE_OUTPUT = 1  # The number of Rx of MIMO

### Actions ###
ACTIONS = ["noa", "syncope"]  # Labeled number (starts from 1) must be matched with the order of this
USE_NOACTIVITY = False  # Set "True" will include NoActivity windows in learning
USE_CUSTOM_NOACTIVITY = True  # Custom NoActivity (Not 0)
CUSTOM_NOACTIVITY_NO = 0  # Index number of custom NoActivity action (0 to len(ACTIONS) - 1)

### Learning Parameters ###
LEARNING_RATE = 0.00001
N_ITERATIONS = 128  # epoch
BATCH_SIZE = 16

### Learning Details ###
KFOLD = 11
N_SKIPROW = 0
N_HIDDEN = 1024  # hidden layer num of features
USE_AMPLITUDE = False  # If true, learner will not remove amplitude from csi
USE_PHASE = True  # If true, learner will not remove phase from csi

### Path ###
SOURCE_DIR = "./Dataset/"
MERGED_DIR = "./Input_WINDOW{0}_COL{1}_TH{2}/"
SOURCE_PATH = SOURCE_DIR + "{0}_{1}*.csv"
MERGED_PATH = MERGED_DIR + "{3}_{4}.csv"
OUTPUT_PATH = "./Output_LR{0}_BATCH{1}_HIDDEN{2}/{3}"
LOG_PATH = "./Log_LR{0}_BATCH{1}_HIDDEN{2}/{3}"


### Fixed Variables ###
N_CLASSES = len(ACTIONS) + 1  # (Fixed) All actions + "No Activity"
N_VALID_CLASSES = len(ACTIONS)  # (Fixed) All actions
PKT_COLUMNS = 30 * MULTIPLE_INPUT * MULTIPLE_OUTPUT  # (Fixed) Get first {PKT_COLUMNS} columns of each packet data
N_COLUMNS = PKT_COLUMNS * (USE_PHASE + USE_AMPLITUDE)  # (Fixed) Total number of CSI columns
COL_START = 1 + (USE_PHASE and not USE_AMPLITUDE) * PKT_COLUMNS  # (Fixed)
